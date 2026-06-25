"""Tests for billing models and the plan catalog."""

from __future__ import annotations

from datetime import datetime, timezone

from bird_mach.billing.models import Plan, Subscription, SubscriptionStatus
from bird_mach.billing.plans import FREE_PLAN_ID, PRO_PLAN_ID, build_catalog


class TestSubscriptionStatus:
    def test_active_and_trialing_grant_access(self):
        assert SubscriptionStatus.ACTIVE.grants_access
        assert SubscriptionStatus.TRIALING.grants_access

    def test_other_statuses_deny_access(self):
        for s in (
            SubscriptionStatus.PAST_DUE,
            SubscriptionStatus.CANCELED,
            SubscriptionStatus.INCOMPLETE,
            SubscriptionStatus.UNPAID,
        ):
            assert not s.grants_access


class TestSubscription:
    def test_is_active_follows_status(self):
        sub = Subscription(id="s1", user_id="u1", plan_id="pro", status=SubscriptionStatus.ACTIVE)
        assert sub.is_active
        sub.status = SubscriptionStatus.CANCELED
        assert not sub.is_active

    def test_public_dict_serialises_period_end(self):
        end = datetime(2026, 7, 1, tzinfo=timezone.utc)
        sub = Subscription(
            id="s1",
            user_id="u1",
            plan_id="pro",
            status=SubscriptionStatus.ACTIVE,
            current_period_end=end,
        )
        d = sub.public_dict()
        assert d["status"] == "active"
        assert d["current_period_end"] == end.isoformat()


class TestCatalog:
    def test_free_plan_present_and_free(self):
        catalog = build_catalog()
        assert catalog[FREE_PLAN_ID].is_free
        assert catalog[FREE_PLAN_ID].stripe_price_id == ""

    def test_pro_plan_uses_injected_price(self):
        catalog = build_catalog(stripe_price_pro="price_123")
        assert catalog[PRO_PLAN_ID].stripe_price_id == "price_123"
        assert not catalog[PRO_PLAN_ID].is_free

    def test_plan_public_dict_hides_stripe_price(self):
        plan = Plan(id="x", name="X", price_cents=100, interval="month", stripe_price_id="secret")
        assert "stripe_price_id" not in plan.public_dict()
