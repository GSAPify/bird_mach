"""Per-client rate limiting for sensitive auth endpoints.

Login and registration are brute-force / enumeration targets, so they get a
tighter budget than general API traffic. This reuses the existing
:class:`bird_mach.rate_limiter.TokenBucketLimiter` keyed by client IP rather
than introducing new infrastructure.
"""

from __future__ import annotations

import time
from collections.abc import Callable

from fastapi import Depends, HTTPException, Request, status

from bird_mach.rate_limiter import TokenBucketLimiter

# Allow a small burst (typos, a retried form) then ~1 attempt every 30s. This
# is deliberately strict: legitimate users rarely hit it, brute-forcers do.
_LOGIN_LIMITER = TokenBucketLimiter(capacity=5, refill_rate=1 / 30)


def get_login_limiter() -> TokenBucketLimiter:
    """Dependency returning the shared login limiter.

    Exposed as a dependency so tests can override it with a fresh limiter
    rather than fighting shared bucket state across cases.
    """
    return _LOGIN_LIMITER


def _client_key(request: Request) -> str:
    # Honour a single proxy hop's X-Forwarded-For; fall back to the socket peer.
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


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
