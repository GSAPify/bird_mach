"""FastAPI wiring for billing, plus the premium-feature paywall dependency."""

from __future__ import annotations

import logging

from fastapi import Depends, HTTPException, status

from bird_mach.auth.dependencies import get_current_user, get_user_repository
from bird_mach.auth.models import User
from bird_mach.auth.store import UserRepository
from bird_mach.billing.plans import build_catalog
from bird_mach.billing.provider import (
    FakePaymentProvider,
    PaymentProvider,
    StripePaymentProvider,
)
from bird_mach.billing.service import BillingService
from bird_mach.billing.store import SqliteSubscriptionRepository
from bird_mach.config import AppConfig
from bird_mach.db import Database

logger = logging.getLogger(__name__)


def _build_provider(config: AppConfig) -> PaymentProvider:
    """Use real Stripe when a key is configured, else an offline fake.

    Running without a Stripe key in production is a misconfiguration; log a
    warning rather than failing the whole app, so non-billing routes still
    serve while billing degrades to offline mode.
    """
    if config.stripe_api_key:
        return StripePaymentProvider(config.stripe_api_key)
    if config.is_production:
        logger.warning("STRIPE_API_KEY unset in production; billing runs in offline mode")
    return FakePaymentProvider()


def build_billing_service(
    config: AppConfig, *, users: UserRepository | None = None
) -> BillingService:
    return BillingService(
        provider=_build_provider(config),
        users=users or get_user_repository(),
        subscriptions=SqliteSubscriptionRepository(Database(config.auth_db_path)),
        catalog=build_catalog(stripe_price_pro=config.stripe_price_pro),
    )


_service: BillingService | None = None


def get_billing_service() -> BillingService:
    global _service
    if _service is None:
        _service = build_billing_service(AppConfig.from_env())
    return _service


def require_subscription(
    user: User = Depends(get_current_user),
    billing: BillingService = Depends(get_billing_service),
) -> User:
    """Paywall: 402 unless the current user has an active subscription."""
    if not billing.is_entitled(user):
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="An active subscription is required for this feature",
        )
    return user
