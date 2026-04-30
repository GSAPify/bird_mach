"""HTTP API for billing: plans, checkout, portal, subscription, and webhooks."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel

from bird_mach.auth.dependencies import get_current_user
from bird_mach.auth.models import User
from bird_mach.billing.dependencies import get_billing_service
from bird_mach.billing.service import BillingService
from bird_mach.config import AppConfig
from bird_mach.exceptions import (
    BillingError,
    PaymentProviderError,
    UserNotFoundError,
    WebhookVerificationError,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/billing", tags=["billing"])

config = AppConfig.from_env()


class CheckoutRequest(BaseModel):
    plan_id: str
    success_url: str | None = None
    cancel_url: str | None = None


class PortalRequest(BaseModel):
    return_url: str | None = None


def _default_url(request: Request, override: str | None, path: str) -> str:
    if override:
        return override
    base = config.render_external_url or str(request.base_url).rstrip("/")
    return f"{base}{path}"


@router.get("/plans")
def list_plans(billing: BillingService = Depends(get_billing_service)) -> dict:
    return {"plans": [p.public_dict() for p in billing._catalog.values()]}


@router.get("/subscription")
def my_subscription(
    user: User = Depends(get_current_user),
    billing: BillingService = Depends(get_billing_service),
) -> dict:
    sub = billing.get_subscription(user)
    return {"subscription": sub.public_dict() if sub else None, "entitled": billing.is_entitled(user)}


@router.post("/checkout")
def create_checkout(
    body: CheckoutRequest,
    request: Request,
    user: User = Depends(get_current_user),
    billing: BillingService = Depends(get_billing_service),
) -> dict:
    try:
        session = billing.start_checkout(
            user,
            body.plan_id,
            success_url=_default_url(request, body.success_url, "/billing/success"),
            cancel_url=_default_url(request, body.cancel_url, "/billing/cancel"),
        )
    except BillingError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    except PaymentProviderError as exc:
        logger.error("checkout failed: %s", exc)
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Payment provider error") from exc
    return {"checkout_url": session.url, "session_id": session.id}


@router.get("/invoices")
def list_invoices(
    user: User = Depends(get_current_user),
    billing: BillingService = Depends(get_billing_service),
) -> dict:
    """Return the caller's recent invoices."""
    try:
        invoices = billing.invoice_history(user)
    except PaymentProviderError as exc:
        logger.error("invoice history failed: %s", exc)
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Payment provider error") from exc
    return {"invoices": invoices}


@router.post("/cancel")
def cancel_subscription(
    user: User = Depends(get_current_user),
    billing: BillingService = Depends(get_billing_service),
) -> dict:
    """Cancel the caller's subscription at the end of the current period."""
    try:
        sub = billing.cancel_subscription(user, at_period_end=True)
    except BillingError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    except PaymentProviderError as exc:
        logger.error("cancel failed: %s", exc)
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Payment provider error") from exc
    return {"status": "cancellation_requested", "subscription": sub.public_dict()}


@router.post("/portal")
def billing_portal(
    body: PortalRequest,
    request: Request,
    user: User = Depends(get_current_user),
    billing: BillingService = Depends(get_billing_service),
) -> dict:
    try:
        url = billing.billing_portal(
            user, return_url=_default_url(request, body.return_url, "/billing")
        )
    except BillingError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    except PaymentProviderError as exc:
        logger.error("portal failed: %s", exc)
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Payment provider error") from exc
    return {"portal_url": url}


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    billing: BillingService = Depends(get_billing_service),
) -> Response:
    """Receive Stripe webhooks. The signature is verified before any state change."""
    payload = await request.body()
    signature = request.headers.get("stripe-signature", "")
    try:
        result = billing.handle_webhook(payload, signature, config.stripe_webhook_secret)
    except WebhookVerificationError as exc:
        # 400 tells Stripe the event was rejected (bad signature / payload).
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid signature") from exc
    except UserNotFoundError as exc:
        # The signature is valid but no local user maps to this customer. That
        # won't resolve on retry, and a non-2xx makes Stripe retry on a
        # schedule (retry storm + dashboard alerts). Acknowledge (200) and log
        # for investigation instead of asking Stripe to keep retrying.
        logger.error("webhook references unknown customer, acknowledging: %s", exc)
        result = "ignored:unknown_customer"
    except BillingError as exc:
        # Signed but malformed (missing ids, unmapped price). Retrying will not
        # change the payload, so acknowledge rather than trigger a retry storm.
        logger.error("webhook payload rejected, acknowledging: %s", exc)
        result = "ignored:bad_payload"
    return Response(content=result, media_type="text/plain")
