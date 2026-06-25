"""Full-stack integration test against the real wired application.

Exercises register → login → free-tier quota → subscribe (webhook) → premium
access, through bird_mach.webapp.app with all routers and middleware mounted,
using in-memory store overrides so nothing touches the on-disk database.
"""

from __future__ import annotations

import io
import json
import wave

import pytest
from fastapi.testclient import TestClient

from bird_mach.auth.dependencies import get_audit_log, get_auth_service
from bird_mach.auth.audit import InMemoryAuditLog
from bird_mach.auth.ratelimit import get_login_limiter
from bird_mach.auth.service import AuthService
from bird_mach.auth.store import InMemoryUserRepository
from bird_mach.auth.tokens import TokenService
from bird_mach.billing.dependencies import get_billing_service
from bird_mach.billing.plans import build_catalog
from bird_mach.billing.provider import FakePaymentProvider
from bird_mach.billing.quota import get_usage_service
from bird_mach.billing.service import BillingService
from bird_mach.billing.store import InMemorySubscriptionRepository
from bird_mach.rate_limiter import TokenBucketLimiter
from bird_mach.usage import InMemoryUsageRepository, UsageService
from bird_mach.webapp import app

SECRET = "integration-secret-at-least-32-bytes!!!!"
PRICE_PRO = "price_pro_test"


def _wav() -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(8000)
        w.writeframes(b"\x00\x01" * 8000)
    return buf.getvalue()


@pytest.fixture
def client():
    users = InMemoryUserRepository()
    subs = InMemorySubscriptionRepository()
    auth = AuthService(users, TokenService(SECRET))
    billing = BillingService(
        provider=FakePaymentProvider(),
        users=users,
        subscriptions=subs,
        catalog=build_catalog(stripe_price_pro=PRICE_PRO),
    )
    usage = UsageService(InMemoryUsageRepository(), free_daily_limit=2)

    app.dependency_overrides[get_auth_service] = lambda: auth
    app.dependency_overrides[get_billing_service] = lambda: billing
    app.dependency_overrides[get_usage_service] = lambda: usage
    app.dependency_overrides[get_audit_log] = lambda: InMemoryAuditLog()
    app.dependency_overrides[get_login_limiter] = lambda: TokenBucketLimiter(
        capacity=1000, refill_rate=1000
    )
    yield TestClient(app), users
    app.dependency_overrides.clear()


def test_full_saas_journey(client):
    c, users = client

    # 1. Register + login.
    assert c.post("/auth/register", json={"email": "n@b.com", "password": "supersecret"}).status_code == 201
    tokens = c.post("/auth/login", json={"email": "n@b.com", "password": "supersecret"}).json()
    h = {"Authorization": f"Bearer {tokens['access_token']}"}

    # 2. Free tier: allowed up to the limit (2), then 402.
    for _ in range(2):
        assert c.post("/api/v1/analyze/metered", files={"file": ("a.wav", _wav())}, headers=h).status_code == 200
    assert c.post("/api/v1/analyze/metered", files={"file": ("a.wav", _wav())}, headers=h).status_code == 402

    # 3. Premium batch is gated until subscribed.
    assert c.post("/api/v1/analyze/batch", files=[("files", ("a.wav", _wav()))], headers=h).status_code == 402

    # 4. Subscribe: checkout attaches a Stripe customer, webhook grants entitlement.
    c.post("/billing/checkout", json={"plan_id": "pro"}, headers=h)
    customer_id = users.get_by_email("n@b.com").stripe_customer_id
    event = json.dumps({
        "type": "customer.subscription.created",
        "data": {"object": {
            "id": "sub_1", "customer": customer_id, "status": "active",
            "current_period_end": 1_900_000_000,
            "items": {"data": [{"price": {"id": PRICE_PRO}}]},
        }},
    }).encode()
    assert c.post("/billing/webhook", content=event, headers={"stripe-signature": "valid"}).status_code == 200

    # 5. Now entitled: premium batch works and metered analysis is unlimited.
    assert c.get("/billing/subscription", headers=h).json()["entitled"] is True
    assert c.post("/api/v1/analyze/batch", files=[("files", ("a.wav", _wav()))], headers=h).status_code == 200
    assert c.post("/api/v1/analyze/metered", files={"file": ("a.wav", _wav())}, headers=h).status_code == 200
