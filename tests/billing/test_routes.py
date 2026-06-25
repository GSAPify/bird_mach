"""End-to-end API tests for the billing router."""

from __future__ import annotations

import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bird_mach.auth.dependencies import get_auth_service
from bird_mach.auth.service import AuthService
from bird_mach.auth.store import InMemoryUserRepository
from bird_mach.auth.tokens import TokenService
from bird_mach.billing.dependencies import get_billing_service
from bird_mach.billing.plans import build_catalog
from bird_mach.billing.provider import FakePaymentProvider
from bird_mach.billing.routes import router
from bird_mach.billing.service import BillingService
from bird_mach.billing.store import InMemorySubscriptionRepository

SECRET = "billing-routes-secret-at-least-32-bytes!"
PRICE_PRO = "price_pro_test"


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
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_auth_service] = lambda: auth
    app.dependency_overrides[get_billing_service] = lambda: billing
    client = TestClient(app)

    auth.register("a@b.com", "supersecret")
    tokens = auth.login("a@b.com", "supersecret")
    headers = {"Authorization": f"Bearer {tokens.access_token}"}
    return client, headers, billing, users


def _sub_event(customer, status="active"):
    return json.dumps(
        {
            "type": "customer.subscription.created",
            "data": {
                "object": {
                    "id": "sub_1",
                    "customer": customer,
                    "status": status,
                    "current_period_end": 1_800_000_000,
                    "items": {"data": [{"price": {"id": PRICE_PRO}}]},
                }
            },
        }
    ).encode()


class TestPlans:
    def test_plans_are_public(self, ctx):
        client, *_ = ctx
        resp = client.get("/billing/plans")
        assert resp.status_code == 200
        ids = {p["id"] for p in resp.json()["plans"]}
        assert {"free", "pro"} <= ids


class TestCheckoutAndSubscription:
    def test_checkout_requires_auth(self, ctx):
        client, *_ = ctx
        assert client.post("/billing/checkout", json={"plan_id": "pro"}).status_code == 401

    def test_checkout_returns_url(self, ctx):
        client, headers, *_ = ctx
        resp = client.post("/billing/checkout", json={"plan_id": "pro"}, headers=headers)
        assert resp.status_code == 200
        assert resp.json()["checkout_url"]

    def test_checkout_free_plan_rejected(self, ctx):
        client, headers, *_ = ctx
        resp = client.post("/billing/checkout", json={"plan_id": "free"}, headers=headers)
        assert resp.status_code == 400

    def test_subscription_status_starts_unentitled(self, ctx):
        client, headers, *_ = ctx
        resp = client.get("/billing/subscription", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["entitled"] is False


class TestWebhook:
    def test_webhook_grants_entitlement(self, ctx):
        client, headers, billing, users = ctx
        # Attach the Stripe customer to the account first (checkout does this).
        client.post("/billing/checkout", json={"plan_id": "pro"}, headers=headers)
        customer_id = users.get_by_email("a@b.com").stripe_customer_id

        resp = client.post(
            "/billing/webhook",
            content=_sub_event(customer_id),
            headers={"stripe-signature": "valid"},
        )
        assert resp.status_code == 200
        assert client.get("/billing/subscription", headers=headers).json()["entitled"] is True

    def test_webhook_bad_signature_rejected(self, ctx):
        client, *_ = ctx
        resp = client.post(
            "/billing/webhook",
            content=b"{}",
            headers={"stripe-signature": "wrong"},
        )
        assert resp.status_code == 400

    def test_webhook_unknown_customer_is_acknowledged(self, ctx):
        # A valid-signature event for a customer with no local user is acked
        # (200) and logged, not 4xx — otherwise Stripe retries forever.
        client, *_ = ctx
        resp = client.post(
            "/billing/webhook",
            content=_sub_event("cus_does_not_exist"),
            headers={"stripe-signature": "valid"},
        )
        assert resp.status_code == 200
        assert resp.text == "ignored:unknown_customer"
