"""The static catalog of product tiers Mach sells.

The free tier always exists. The paid tier's Stripe Price ID comes from config
(``STRIPE_PRICE_PRO``) so the same code runs against test-mode and live-mode
Stripe accounts without edits.
"""

from __future__ import annotations

from bird_mach.billing.models import Plan

FREE_PLAN_ID = "free"
PRO_PLAN_ID = "pro"

FREE_PLAN = Plan(
    id=FREE_PLAN_ID,
    name="Free",
    price_cents=0,
    interval="month",
    features=(
        "Up to 5 analyses per day",
        "Standard audio embeddings",
        "Community support",
    ),
)


def build_catalog(stripe_price_pro: str = "") -> dict[str, Plan]:
    """Return the plan catalog keyed by plan id.

    ``stripe_price_pro`` is injected from config so the Pro plan points at the
    correct Stripe Price for the active environment.
    """
    pro = Plan(
        id=PRO_PLAN_ID,
        name="Pro",
        price_cents=1900,
        interval="month",
        stripe_price_id=stripe_price_pro,
        features=(
            "Unlimited analyses",
            "High-resolution spectral embeddings",
            "Batch processing & priority queue",
            "Email support",
        ),
    )
    return {FREE_PLAN_ID: FREE_PLAN, PRO_PLAN_ID: pro}
