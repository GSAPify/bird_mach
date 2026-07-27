"""Per-client rate limiting for sensitive auth endpoints.

Login and registration are brute-force / enumeration targets, so they get a
tighter budget than general API traffic. This reuses the existing
:class:`bird_mach.rate_limiter.TokenBucketLimiter` keyed by client IP rather
than introducing new infrastructure.
"""

from __future__ import annotations

import ipaddress
import os
import time
from collections.abc import Callable
from functools import lru_cache

from fastapi import Depends, HTTPException, Request, status

from bird_mach.rate_limiter import TokenBucketLimiter

#: Comma-separated IPs/CIDRs of proxies allowed to set X-Forwarded-For.
#: Empty (the default) means trust nothing — anyone can forge the header, so
#: an unconfigured deployment must key off the socket peer only.
TRUSTED_PROXIES_ENV = "TRUSTED_PROXY_IPS"

# Allow a small burst (typos, a retried form) then ~1 attempt every 30s. This
# is deliberately strict: legitimate users rarely hit it, brute-forcers do.
_LOGIN_LIMITER = TokenBucketLimiter(capacity=5, refill_rate=1 / 30)


def get_login_limiter() -> TokenBucketLimiter:
    """Dependency returning the shared login limiter.

    Exposed as a dependency so tests can override it with a fresh limiter
    rather than fighting shared bucket state across cases.
    """
    return _LOGIN_LIMITER


@lru_cache(maxsize=8)
def parse_trusted_proxies(raw: str) -> tuple[ipaddress.IPv4Network | ipaddress.IPv6Network, ...]:
    """Parse the allowlist env value into networks; unparseable entries are dropped."""
    networks = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            networks.append(ipaddress.ip_network(part, strict=False))
        except ValueError:
            continue
    return tuple(networks)


def is_trusted_proxy(host: str | None) -> bool:
    """True if ``host`` is an IP inside the configured trusted-proxy allowlist."""
    if not host:
        return False
    networks = parse_trusted_proxies(os.getenv(TRUSTED_PROXIES_ENV, ""))
    if not networks:
        return False
    try:
        addr = ipaddress.ip_address(host)
    except ValueError:
        return False
    return any(addr in network for network in networks)


def client_ip(request: Request) -> str | None:
    """Resolve the real client IP.

    ``X-Forwarded-For`` is attacker-controlled unless the immediate peer is a
    proxy we trust, so it is ignored entirely otherwise. When the peer *is*
    trusted, the chain is walked right-to-left: entries appended by trusted
    proxies are skipped and the first untrusted hop is the closest address we
    can actually attribute to the client. The leftmost entry is never used —
    that is the one the attacker gets to write.
    """
    peer = request.client.host if request.client else None
    if not is_trusted_proxy(peer):
        return peer
    forwarded = request.headers.get("x-forwarded-for")
    if not forwarded:
        return peer
    for hop in reversed(forwarded.split(",")):
        hop = hop.strip()
        if hop and not is_trusted_proxy(hop):
            return hop
    return peer


def _client_key(request: Request) -> str:
    return client_ip(request) or "unknown"


def rate_limit(limiter: TokenBucketLimiter) -> Callable[[Request], None]:
    """Build a FastAPI dependency that enforces a fixed ``limiter`` per IP."""

    def _dependency(request: Request) -> None:
        _enforce(limiter, request)

    return _dependency


def login_rate_limit(
    request: Request, limiter: TokenBucketLimiter = Depends(get_login_limiter)
) -> None:
    """Rate-limit dependency for auth endpoints, using the injectable limiter."""
    _enforce(limiter, request)


def _enforce(limiter: TokenBucketLimiter, request: Request) -> None:
    result = limiter.check(_client_key(request))
    if not result.allowed:
        retry_after = max(1, int(result.reset_at - time.time()))
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many attempts; please slow down",
            headers={"Retry-After": str(retry_after)},
        )
