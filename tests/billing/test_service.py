"""Tests for the billing service, including the webhook → entitlement flow."""

from __future__ import annotations

import json

import pytest

from bird_mach.auth.models import User
from bird_mach.auth.store import InMemoryUserRepository
from bird_mach.billing.plans import build_catalog
from bird_mach.billing.provider import FakePaymentProvider
from bird_mach.billing.service import BillingService
from bird_mach.billing.store import InMemorySubscriptionRepository
from bird_mach.exceptions import BillingError, UserNotFoundError

PRICE_PRO = "price_pro_test"


@pytest.fixture
def env():
    users = InMemoryUserRepository()
    subs = InMemorySubscriptionRepository()
    provider = FakePaymentProvider()
    svc = BillingService(
        provider=provider,
        users=users,
        subscriptions=subs,
        catalog=build_catalog(stripe_price_pro=PRICE_PRO),
    )
    user = User(id="u1", email="a@b.com", password_hash="x")
    users.add(user)
    return svc, user, users, subs, provider


def _sub_event(event_type, *, sub_id="sub_1", customer="cus_1", status="active"):
    return json.dumps(
        {
            "type": event_type,
            "data": {
                "object": {
                    "id": sub_id,
                    "customer": customer,
                    "status": status,
                    "current_period_end": 1_800_000_000,
                    "items": {"data": [{"price": {"id": PRICE_PRO}}]},
                }
            },
        }
    ).encode()


class TestCustomerAndCheckout:
    def test_ensure_customer_creates_once(self, env):
        svc, user, users, _, provider = env
        cid = svc.ensure_customer(user)
        assert cid.startswith("cus_fake_")
        assert users.get("u1").stripe_customer_id == cid
        # Second call reuses the same customer.
        assert svc.ensure_customer(user) == cid
        assert len(provider.customers) == 1

    def test_start_checkout_returns_session(self, env):
        svc, user, *_ = env
        session = svc.start_checkout(
            user, "pro", success_url="https://x/ok", cancel_url="https://x/no"
        )
        assert session.url

    def test_cannot_checkout_free_plan(self, env):
        svc, user, *_ = env
        with pytest.raises(BillingError):
            svc.start_checkout(user, "free", success_url="https://x", cancel_url="https://x")

    def test_unknown_plan_rejected(self, env):
        svc, user, *_ = env
        with pytest.raises(BillingError):
            svc.start_checkout(user, "ghost", success_url="https://x", cancel_url="https://x")

    def test_portal_requires_customer(self, env):
        svc, user, *_ = env
        with pytest.raises(BillingError):
            svc.billing_portal(user, return_url="https://x")
        svc.ensure_customer(user)
        assert svc.billing_portal(user, return_url="https://x").startswith("https://")


class TestWebhookEntitlement:
    def _attach_customer(self, svc, user, users, customer="cus_1"):
        user.stripe_customer_id = customer
        users.update(user)

    def test_active_subscription_grants_entitlement(self, env):
        svc, user, users, _, _ = env
        self._attach_customer(svc, user, users)
        assert not svc.is_entitled(user)
        svc.handle_webhook(_sub_event("customer.subscription.created"), "valid", "whsec")
        assert svc.is_entitled(user)
        sub = svc.get_subscription(user)
        assert sub.plan_id == "pro"
        assert sub.current_period_end is not None

    def test_canceled_subscription_revokes_entitlement(self, env):
        svc, user, users, _, _ = env
        self._attach_customer(svc, user, users)
        svc.handle_webhook(_sub_event("customer.subscription.created"), "valid", "whsec")
        svc.handle_webhook(_sub_event("customer.subscription.deleted"), "valid", "whsec")
        assert not svc.is_entitled(user)

    def test_past_due_denies_access(self, env):
        svc, user, users, _, _ = env
        self._attach_customer(svc, user, users)
        svc.handle_webhook(
            _sub_event("customer.subscription.updated", status="past_due"), "valid", "whsec"
        )
        assert not svc.is_entitled(user)

    def test_replayed_webhook_is_idempotent(self, env):
        svc, user, users, subs, _ = env
        self._attach_customer(svc, user, users)
        event = _sub_event("customer.subscription.created")
        svc.handle_webhook(event, "valid", "whsec")
        svc.handle_webhook(event, "valid", "whsec")
        assert subs.get_by_user("u1") is not None
        # Same subscription id → one record, not two.
        assert subs.get("sub_1") is not None

    def test_unhandled_event_ignored(self, env):
        svc, *_ = env
        result = svc.handle_webhook(
            json.dumps({"type": "invoice.paid", "data": {"object": {}}}).encode(),
            "valid",
            "whsec",
        )
        assert result == "ignored"

    def test_webhook_for_unknown_customer_raises(self, env):
        svc, *_ = env
        with pytest.raises(UserNotFoundError):
            svc.handle_webhook(
                _sub_event("customer.subscription.created", customer="cus_unknown"),
                "valid",
                "whsec",
            )
