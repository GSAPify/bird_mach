"""Tests for auth rate limiting."""

from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from bird_mach.auth.ratelimit import rate_limit
from bird_mach.rate_limiter import TokenBucketLimiter


def _make_client(capacity: int) -> TestClient:
    app = FastAPI()
    limiter = TokenBucketLimiter(capacity=capacity, refill_rate=1 / 3600)

    @app.get("/limited", dependencies=[Depends(rate_limit(limiter))])
    def limited():
        return {"ok": True}

    return TestClient(app)


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


def test_separate_clients_have_separate_budgets():
    client = _make_client(capacity=1)
    assert client.get("/limited", headers={"X-Forwarded-For": "1.1.1.1"}).status_code == 200
    # Different forwarded IP → fresh bucket.
    assert client.get("/limited", headers={"X-Forwarded-For": "2.2.2.2"}).status_code == 200
    # Same IP again → blocked.
    assert client.get("/limited", headers={"X-Forwarded-For": "1.1.1.1"}).status_code == 429
