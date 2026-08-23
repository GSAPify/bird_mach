"""Billing domain models: plans and subscriptions.

Plans are a small static catalog (the product tiers Mach sells). Subscriptions
are durable per-user records mirrored from the payment provider so the app can
answer "is this user entitled to premium features?" without a network call to
Stripe on every request.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone


class SubscriptionStatus(str, enum.Enum):
    """Mirrors the Stripe subscription statuses we act on.

    ``ACTIVE`` and ``TRIALING`` grant entitlement; everything else does not.
    """

    ACTIVE = "active"
    TRIALING = "trialing"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    INCOMPLETE = "incomplete"
    UNPAID = "unpaid"

    @property
    def grants_access(self) -> bool:
        return self in {SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING}


@dataclass(frozen=True)
class Plan:
    """A purchasable product tier."""

    id: str
    name: str
    price_cents: int
    interval: str  # "month" | "year"
    # The Stripe Price ID this plan maps to; empty for the free tier.
    stripe_price_id: str = ""
    features: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.price_cents < 0:
            raise ValueError("price_cents must not be negative")
        if self.interval not in {"month", "year"}:
            raise ValueError("interval must be 'month' or 'year'")

    @property
    def is_free(self) -> bool:
        return self.price_cents == 0

    def public_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "price_cents": self.price_cents,
            "interval": self.interval,
            "features": list(self.features),
        }


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Subscription:
    """A user's current subscription state, mirrored from the provider."""

    id: str
    user_id: str
    plan_id: str
    status: SubscriptionStatus
    stripe_subscription_id: str | None = None
    current_period_end: datetime | None = None
    created_at: datetime = field(default_factory=_now)

    @property
    def is_active(self) -> bool:
        # A stale row can still say "active" if the renewal webhook never
        # arrived, so the period end is authoritative when we have one.
        if not self.status.grants_access:
            return False
        return self.current_period_end is None or _now() < self.current_period_end

    def public_dict(self) -> dict:
        return {
            "id": self.id,
            "plan_id": self.plan_id,
            "status": self.status.value,
            "is_active": self.is_active,
            "current_period_end": (
                self.current_period_end.isoformat() if self.current_period_end else None
            ),
        }
