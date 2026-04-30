"""Authenticated API: metered analysis, premium batch, and usage reporting.

These routes turn the auth + billing layers into actual product behaviour:

* ``/api/v1/analyze`` (metered) counts against the free-tier daily quota and
  is unlimited for subscribers.
* ``/api/v1/analyze/batch`` is gated behind ``require_subscription`` — a real
  premium feature, not a decorative paywall.
* ``/api/v1/account/usage`` reports the caller's remaining free-tier quota.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile

from bird_mach.api.routes import analyze_bytes, read_capped
from bird_mach.api.schemas import AnalysisSummaryResponse
from bird_mach.auth.dependencies import get_current_user
from bird_mach.auth.models import User
from bird_mach.billing.dependencies import get_billing_service, require_subscription
from bird_mach.billing.quota import enforce_analysis_quota, get_usage_service
from bird_mach.billing.service import BillingService
from bird_mach.usage import UsageService

router = APIRouter(prefix="/api/v1", tags=["account"])


@router.post("/analyze/metered", response_model=AnalysisSummaryResponse)
async def metered_analyze(
    file: UploadFile = File(...),
    sr: int = 22050,
    user: User = Depends(enforce_analysis_quota),
):
    """Analyze one file, counting against the caller's daily quota."""
    contents = await read_capped(file)
    return analyze_bytes(contents, sr)


@router.post("/analyze/batch", response_model=list[AnalysisSummaryResponse])
async def batch_analyze(
    files: list[UploadFile] = File(...),
    sr: int = 22050,
    user: User = Depends(require_subscription),
):
    """Premium: analyze multiple files in one request. Requires a subscription."""
    results = []
    for f in files:
        results.append(analyze_bytes(await read_capped(f), sr))
    return results


@router.get("/account/usage")
def account_usage(
    user: User = Depends(get_current_user),
    billing: BillingService = Depends(get_billing_service),
    usage: UsageService = Depends(get_usage_service),
) -> dict:
    entitled = billing.is_entitled(user)
    return {
        "entitled": entitled,
        "free_daily_limit": usage.free_daily_limit,
        "used_today": usage.used_today(user.id),
        "remaining_today": None if entitled else usage.remaining_for_free_tier(user.id),
    }
