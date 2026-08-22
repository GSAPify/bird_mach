"""Billing orchestration: customers, checkout, portal, and webhook handling.

This is the only layer that combines the payment provider, the user
repository (to attach a Stripe customer to an account), the subscription
repository (durable entitlement state), and the plan catalog.

Subscription records are created and updated exclusively from verified
webhooks, keyed by the Stripe subscription id. That keeps the app's view of
"who is entitled" in lock-step with Stripe and makes replayed webhooks
idempotent rather than duplicative.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from bird_mach.auth.models import User
from bird_mach.auth.store import UserRepository
from bird_mach.billing.models import Plan, Subscription, SubscriptionStatus
from bird_mach.billing.provider import CheckoutSession, PaymentProvider
from bird_mach.billing.store import SubscriptionRepository
from bird_mach.exceptions import BillingError, UserNotFoundError

logger = logging.getLogger(__name__)

# Stripe subscription events we act on.
_SUBSCRIPTION_EVENTS = {
    "customer.subscription.created",
    "customer.subscription.updated",
    "customer.subscription.deleted",
}


class BillingService:
    def __init__(
        self,
        *,
        provider: PaymentProvider,
        users: UserRepository,
        subscriptions: SubscriptionRepository,
        catalog: dict[str, Plan],
    ) -> None:
        self._provider = provider
        self._users = users
        self._subs = subscriptions
        self._catalog = catalog
        # Reverse map Stripe Price id -> plan id, for resolving webhook payloads.
        self._price_to_plan = {
            plan.stripe_price_id: plan.id
            for plan in catalog.values()
            if plan.stripe_price_id
        }

    def get_plan(self, plan_id: str) -> Plan:
        plan = self._catalog.get(plan_id)
        if plan is None:
            raise BillingError(f"unknown plan: {plan_id}")
        return plan

    def ensure_customer(self, user: User) -> str:
        """Return the user's Stripe customer id, creating one on first use."""
        if user.stripe_customer_id:
            return user.stripe_customer_id
        customer_id = self._provider.create_customer(
            user.email, metadata={"user_id": user.id}
        )
        user.stripe_customer_id = customer_id
        self._users.update(user)
        return customer_id

    def start_checkout(
        self, user: User, plan_id: str, *, success_url: str, cancel_url: str
    ) -> CheckoutSession:
        plan = self.get_plan(plan_id)
        if plan.is_free or not plan.stripe_price_id:
            raise BillingError(f"plan {plan_id!r} is not purchasable")
        customer_id = self.ensure_customer(user)
        return self._provider.create_checkout_session(
            customer_id=customer_id,
            price_id=plan.stripe_price_id,
            success_url=success_url,
            cancel_url=cancel_url,
        )

    def billing_portal(self, user: User, *, return_url: str) -> str:
        if not user.stripe_customer_id:
            raise BillingError("user has no billing account yet")
        return self._provider.create_billing_portal_session(
            customer_id=user.stripe_customer_id, return_url=return_url
        )

    def cancel_subscription(self, user: User, *, at_period_end: bool = True) -> Subscription:
        """Request cancellation of the user's active subscription.

        Delegates to the provider; the authoritative status change still
        arrives via the subscription webhook, so we don't optimistically flip
        local state to canceled here (that would briefly under-report access
        the user has already paid for through the period end).
        """
        sub = self._subs.get_by_user(user.id)
        if sub is None or not sub.is_active or not sub.stripe_subscription_id:
            raise BillingError("no active subscription to cancel")
        self._provider.cancel_subscription(
            sub.stripe_subscription_id, at_period_end=at_period_end
        )
        return sub

    def invoice_history(self, user: User, *, limit: int = 20) -> list[dict]:
        """Return the user's recent invoices, or [] if they have no customer yet."""
        if limit < 1:
            raise ValueError("limit must be at least 1")
        if not user.stripe_customer_id:
            return []
        return self._provider.list_invoices(user.stripe_customer_id, limit=limit)

    def get_subscription(self, user: User) -> Subscription | None:
        return self._subs.get_by_user(user.id)

    def is_entitled(self, user: User) -> bool:
        """True if the user currently has an access-granting subscription."""
        sub = self._subs.get_by_user(user.id)
        return sub is not None and sub.is_active

    def handle_webhook(self, payload: bytes, signature: str, secret: str) -> str:
        """Verify and process a provider webhook. Returns a short status string.

        Unknown event types are acknowledged and ignored so Stripe does not
        retry events we simply don't care about.
        """
        event = self._provider.verify_webhook(payload, signature, secret)
        if event.type not in _SUBSCRIPTION_EVENTS:
            logger.debug("ignoring unhandled webhook event: %s", event.type)
            return "ignored"
        return self._apply_subscription_event(event.type, event.data.get("object", {}))

    def _apply_subscription_event(self, event_type: str, obj: dict) -> str:
        stripe_sub_id = obj.get("id")
        customer_id = obj.get("customer")
        if not stripe_sub_id or not customer_id:
            raise BillingError("subscription webhook missing id/customer")

        user = self._users.get_by_stripe_customer_id(customer_id)
        if user is None:
            # Customer exists in Stripe but not locally — surface rather than
            # silently dropping a paying customer's state.
            raise UserNotFoundError(f"no user for stripe customer {customer_id}")

        if event_type == "customer.subscription.deleted":
            status = SubscriptionStatus.CANCELED
        else:
            status = self._parse_status(obj.get("status"))

        self._subs.upsert(
            Subscription(
                id=stripe_sub_id,
                user_id=user.id,
                plan_id=self._plan_from_object(obj),
                status=status,
                stripe_subscription_id=stripe_sub_id,
                current_period_end=self._parse_period_end(obj.get("current_period_end")),
            )
        )
        return f"applied:{status.value}"

    @staticmethod
    def _parse_status(raw: str | None) -> SubscriptionStatus:
        try:
            return SubscriptionStatus(raw)
        except ValueError:
            # Statuses we don't model (e.g. "paused") are treated as no-access.
            return SubscriptionStatus.INCOMPLETE

    def _plan_from_object(self, obj: dict) -> str:
        items = (obj.get("items") or {}).get("data") or []
        if not items:
            raise BillingError("subscription object has no line items")
        price = items[0].get("price")
        price_id = price.get("id") if isinstance(price, dict) else None
        if price_id not in self._price_to_plan:
            # Guessing "pro" here would write the wrong plan_id and hide a
            # catalog/config mismatch until a customer complains.
            raise BillingError(f"unmapped Stripe price {price_id!r}")
        return self._price_to_plan[price_id]

    @staticmethod
    def _parse_period_end(raw: int | None) -> datetime | None:
        if raw is None:
            return None
        return datetime.fromtimestamp(raw, tz=timezone.utc)
