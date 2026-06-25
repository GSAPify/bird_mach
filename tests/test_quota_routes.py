"""End-to-end tests that the paywall and quota gate real endpoints."""

from __future__ import annotations

import io
import wave

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bird_mach.api.account import router
from bird_mach.auth.dependencies import get_auth_service
from bird_mach.auth.service import AuthService
from bird_mach.auth.store import InMemoryUserRepository
from bird_mach.auth.tokens import TokenService
from bird_mach.billing.dependencies import get_billing_service
from bird_mach.billing.plans import build_catalog
from bird_mach.billing.provider import FakePaymentProvider
from bird_mach.billing.quota import get_usage_service
from bird_mach.billing.service import BillingService
from bird_mach.billing.store import InMemorySubscriptionRepository
from bird_mach.usage import InMemoryUsageRepository, UsageService

SECRET = "quota-routes-secret-at-least-32-bytes!!!"
PRICE_PRO = "price_pro_test"


def _wav_bytes() -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(8000)
        w.writeframes(b"\x00\x01" * 8000)
    return buf.getvalue()


@pytest.fixture
def ctx():
    users = InMemoryUserRepository()
    subs = InMemorySubscriptionRepository()
    auth = AuthService(users, TokenService(SECRET))
    billing = BillingService(
        provider=FakePaymentProvider(),
        users=users,
        subscriptions=subs,
        catalog=build_catalog(stripe_price_pro=PRICE_PRO),
    )
    usage = UsageService(InMemoryUsageRepository(), free_daily_limit=3)

    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_auth_service] = lambda: auth
    app.dependency_overrides[get_billing_service] = lambda: billing
    app.dependency_overrides[get_usage_service] = lambda: usage
    client = TestClient(app)

    auth.register("a@b.com", "supersecret")
    tokens = auth.login("a@b.com", "supersecret")
    headers = {"Authorization": f"Bearer {tokens.access_token}"}
    return client, headers, billing, subs, users


def _grant_subscription(subs, users):
    from bird_mach.billing.models import Subscription, SubscriptionStatus

    user_id = users.get_by_email("a@b.com").id
    subs.upsert(
        Subscription(id="s1", user_id=user_id, plan_id="pro", status=SubscriptionStatus.ACTIVE)
    )


class TestMeteredAnalyze:
    def test_requires_auth(self, ctx):
        client, *_ = ctx
        resp = client.post("/api/v1/analyze/metered", files={"file": ("a.wav", _wav_bytes())})
        assert resp.status_code == 401

    def test_free_user_blocked_after_quota(self, ctx):
        client, headers, *_ = ctx
        wav = _wav_bytes()
        for _ in range(3):  # free_daily_limit=3
            assert client.post(
                "/api/v1/analyze/metered", files={"file": ("a.wav", wav)}, headers=headers
            ).status_code == 200
        resp = client.post(
            "/api/v1/analyze/metered", files={"file": ("a.wav", wav)}, headers=headers
        )
        assert resp.status_code == 402
        assert "Upgrade" in resp.json()["detail"]

    def test_subscriber_is_unlimited(self, ctx):
        client, headers, _, subs, users = ctx
        # NB: get_current_user resolves the user by id "u1" from the shared repo.
        users.get_by_email("a@b.com")  # ensure exists
        _grant_subscription(subs, users)
        wav = _wav_bytes()
        for _ in range(6):  # well past the free limit of 3
            assert client.post(
                "/api/v1/analyze/metered", files={"file": ("a.wav", wav)}, headers=headers
            ).status_code == 200


class TestPremiumBatch:
    def test_batch_requires_subscription(self, ctx):
        client, headers, *_ = ctx
        resp = client.post(
            "/api/v1/analyze/batch",
            files=[("files", ("a.wav", _wav_bytes()))],
            headers=headers,
        )
        assert resp.status_code == 402

    def test_batch_allowed_for_subscriber(self, ctx):
        client, headers, _, subs, users = ctx
        _grant_subscription(subs, users)
        resp = client.post(
            "/api/v1/analyze/batch",
            files=[
                ("files", ("a.wav", _wav_bytes())),
                ("files", ("b.wav", _wav_bytes())),
            ],
            headers=headers,
        )
        assert resp.status_code == 200
        assert len(resp.json()) == 2


class TestUsageEndpoint:
    def test_usage_reports_remaining(self, ctx):
        client, headers, *_ = ctx
        client.post("/api/v1/analyze/metered", files={"file": ("a.wav", _wav_bytes())}, headers=headers)
        body = client.get("/api/v1/account/usage", headers=headers).json()
        assert body["used_today"] == 1
        assert body["remaining_today"] == 2
        assert body["entitled"] is False
