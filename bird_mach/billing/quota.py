"""Free-tier quota enforcement, tying usage metering to entitlement.

Subscribers are unlimited; free accounts are capped per UTC day. This lives in
the billing package because it depends on both the current user (auth) and
their entitlement (billing) — placing it here avoids an auth→billing import
cycle.
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, status

from bird_mach.auth.dependencies import get_current_user
from bird_mach.auth.models import User
from bird_mach.billing.dependencies import get_billing_service
from bird_mach.billing.service import BillingService
from bird_mach.config import AppConfig
from bird_mach.db import Database
from bird_mach.usage import SqliteUsageRepository, UsageService

_usage: UsageService | None = None


def get_usage_service() -> UsageService:
    global _usage
    if _usage is None:
        _usage = UsageService(SqliteUsageRepository(Database(AppConfig.from_env().auth_db_path)))
    return _usage


def enforce_analysis_quota(
    user: User = Depends(get_current_user),
    billing: BillingService = Depends(get_billing_service),
    usage: UsageService = Depends(get_usage_service),
) -> User:
    """Allow the request, recording usage; 402 if a free user is over quota.

    Entitled (subscribed) users are never blocked. Free users are blocked once
    they hit the daily limit, with a message pointing at the upgrade path.
    """
    if not billing.is_entitled(user) and usage.free_tier_exhausted(user.id):
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=(
                f"Free tier limit of {usage.free_daily_limit} analyses/day reached. "
                "Upgrade to Pro for unlimited analyses."
            ),
        )
    usage.record(user.id)
    return user
