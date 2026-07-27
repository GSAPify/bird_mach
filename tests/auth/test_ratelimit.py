"""Tests for auth rate limiting."""

from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from bird_mach.auth.audit import InMemoryAuditLog
from bird_mach.auth.dependencies import get_audit_log, get_auth_service
from bird_mach.auth.ratelimit import get_login_limiter, rate_limit
from bird_mach.auth.routes import router
from bird_mach.auth.service import AuthService
from bird_mach.auth.store import InMemoryUserRepository
from bird_mach.auth.tokens import TokenService
from bird_mach.rate_limiter import TokenBucketLimiter

SECRET = "ratelimit-test-secret-at-least-32-bytes!"


def _make_client(capacity: int, peer: str = "testclient") -> TestClient:
    app = FastAPI()
    limiter = TokenBucketLimiter(capacity=capacity, refill_rate=1 / 3600)

    @app.get("/limited", dependencies=[Depends(rate_limit(limiter))])
    def limited():
        return {"ok": True}

    return TestClient(app, client=(peer, 40000))


def test_allows_up_to_capacity():
    client = _make_client(capacity=3)
    for _ in range(3):
        assert client.get("/limited").status_code == 200


def test_blocks_after_capacity_with_retry_after():
    client = _make_client(capacity=2)
    client.get("/limited")
    client.get("/limited")
    resp = client.get("/limited")
    assert resp.status_code == 429
    assert int(resp.headers["Retry-After"]) >= 1


def test_rotating_forwarded_for_cannot_bypass_limit_from_untrusted_peer(monkeypatch):
    """The brute-force bypass: one attacker rotating X-Forwarded-For per attempt.

    With no trusted proxy configured the header is forgeable, so it must be
    ignored entirely and every attempt must share the socket peer's bucket.
    """
    monkeypatch.delenv("TRUSTED_PROXY_IPS", raising=False)
    client = _make_client(capacity=5, peer="203.0.113.7")
    codes = [
        client.get("/limited", headers={"X-Forwarded-For": f"1.2.3.{n}"}).status_code
        for n in range(12)
    ]
    assert codes == [200] * 5 + [429] * 7


def test_forwarded_for_honoured_only_when_peer_is_trusted(monkeypatch):
    """The peer, not the header, decides whether X-Forwarded-For counts.

    The same header values are sent from a trusted and an untrusted peer; only
    the trusted one gets per-forwarded-client buckets.
    """
    monkeypatch.setenv("TRUSTED_PROXY_IPS", "10.0.0.0/8")

    proxied = _make_client(capacity=1, peer="10.1.2.3")
    assert proxied.get("/limited", headers={"X-Forwarded-For": "1.1.1.1"}).status_code == 200
    # Different real client behind the same proxy → its own budget.
    assert proxied.get("/limited", headers={"X-Forwarded-For": "2.2.2.2"}).status_code == 200
    # First client again → its own budget is spent.
    assert proxied.get("/limited", headers={"X-Forwarded-For": "1.1.1.1"}).status_code == 429

    # Peer outside the allowlist: the header is ignored, so both requests share
    # the peer's single-token bucket and the second is blocked.
    direct = _make_client(capacity=1, peer="203.0.113.7")
    assert direct.get("/limited", headers={"X-Forwarded-For": "1.1.1.1"}).status_code == 200
    assert direct.get("/limited", headers={"X-Forwarded-For": "2.2.2.2"}).status_code == 429


def test_trusted_proxy_uses_rightmost_untrusted_hop(monkeypatch):
    """Attacker-written entries sit to the left; only the proxy-appended hop counts."""
    monkeypatch.setenv("TRUSTED_PROXY_IPS", "10.0.0.0/8")
    client = _make_client(capacity=1, peer="10.1.2.3")
    # Attacker prepends a forged address; the proxy appends the true client.
    forged = {"X-Forwarded-For": "9.9.9.9, 5.5.5.5"}
    assert client.get("/limited", headers=forged).status_code == 200
    # Rotating the forged left-hand entry must not buy a fresh bucket, because
    # the key comes from the rightmost untrusted hop (5.5.5.5) either way.
    rotated = {"X-Forwarded-For": "8.8.8.8, 5.5.5.5"}
    assert client.get("/limited", headers=rotated).status_code == 429


def test_audit_log_records_real_peer_not_forged_header(monkeypatch):
    """A forged X-Forwarded-For must not end up in the security audit trail."""
    monkeypatch.delenv("TRUSTED_PROXY_IPS", raising=False)
    app = FastAPI()
    app.include_router(router)
    service = AuthService(InMemoryUserRepository(), TokenService(SECRET))
    app.dependency_overrides[get_auth_service] = lambda: service
    app.dependency_overrides[get_login_limiter] = lambda: TokenBucketLimiter(
        capacity=1000, refill_rate=1000
    )
    audit = InMemoryAuditLog()
    app.dependency_overrides[get_audit_log] = lambda: audit
    client = TestClient(app, client=("203.0.113.7", 40000))

    resp = client.post(
        "/auth/register",
        json={"email": "a@b.com", "password": "supersecret"},
        headers={"X-Forwarded-For": "1.2.3.4"},
    )
    assert resp.status_code == 201
    events = audit.recent_for_user(resp.json()["id"])
    assert [e.ip for e in events] == ["203.0.113.7"]
