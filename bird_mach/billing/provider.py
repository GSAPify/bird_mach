"""Payment provider abstraction.

The :class:`PaymentProvider` protocol isolates the rest of the billing code
from Stripe specifics. Two implementations exist:

* :class:`FakePaymentProvider` - deterministic, network-free, for tests and a
  local "offline" mode when no Stripe key is configured.
* :class:`StripePaymentProvider` - the real integration via the ``stripe`` SDK.

Webhook signatures are verified with ``stripe.Webhook.construct_event`` rather
than a hand-rolled HMAC check, which is where signature bugs tend to live.
"""

from __future__ import annotations

import hmac
import itertools
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

from bird_mach.exceptions import PaymentProviderError, WebhookVerificationError


@dataclass(frozen=True)
class CheckoutSession:
    id: str
    url: str


@dataclass(frozen=True)
class WebhookEvent:
    """A verified provider event, normalised to the fields we consume."""

    type: str
    data: dict


class PaymentProvider(ABC):
    @abstractmethod
    def create_customer(self, email: str, *, metadata: dict | None = None) -> str:
        """Create a customer and return its provider id."""

    @abstractmethod
    def create_checkout_session(
        self, *, customer_id: str, price_id: str, success_url: str, cancel_url: str
    ) -> CheckoutSession: ...

    @abstractmethod
    def create_billing_portal_session(self, *, customer_id: str, return_url: str) -> str:
        """Return a URL to the customer's self-service billing portal."""

    @abstractmethod
    def cancel_subscription(self, subscription_id: str, *, at_period_end: bool = True) -> None:
        """Cancel a subscription, by default at the end of the paid period."""

    @abstractmethod
    def list_invoices(self, customer_id: str, *, limit: int = 20) -> list[dict]:
        """Return the customer's recent invoices, newest first."""

    @abstractmethod
    def verify_webhook(self, payload: bytes, signature: str, secret: str) -> WebhookEvent:
        """Verify a webhook signature and return the parsed event."""


class FakePaymentProvider(PaymentProvider):
    """Deterministic in-process provider for tests and offline mode.

    It records calls so tests can assert on them and accepts any webhook whose
    signature equals ``"valid"`` (the payload is treated as already-parsed JSON
    bytes), which lets webhook handling be tested without real Stripe signing.
    """

    def __init__(self) -> None:
        self._ids = itertools.count(1)
        self.customers: list[dict] = []
        self.checkouts: list[dict] = []
        self.portal_sessions: list[dict] = []
        self.cancellations: list[dict] = []
        # Pre-seeded by tests via add_invoice(); keyed by customer id.
        self.invoices: dict[str, list[dict]] = {}

    def create_customer(self, email: str, *, metadata: dict | None = None) -> str:
        cid = f"cus_fake_{next(self._ids)}"
        self.customers.append({"id": cid, "email": email, "metadata": metadata or {}})
        return cid

    def create_checkout_session(
        self, *, customer_id: str, price_id: str, success_url: str, cancel_url: str
    ) -> CheckoutSession:
        sid = f"cs_fake_{next(self._ids)}"
        self.checkouts.append(
            {"id": sid, "customer": customer_id, "price": price_id}
        )
        return CheckoutSession(id=sid, url=f"https://fake.stripe/checkout/{sid}")

    def create_billing_portal_session(self, *, customer_id: str, return_url: str) -> str:
        sid = f"bps_fake_{next(self._ids)}"
        self.portal_sessions.append({"id": sid, "customer": customer_id})
        return f"https://fake.stripe/portal/{sid}"

    def cancel_subscription(self, subscription_id: str, *, at_period_end: bool = True) -> None:
        self.cancellations.append({"id": subscription_id, "at_period_end": at_period_end})

    def add_invoice(self, customer_id: str, invoice: dict) -> None:
        """Test helper: seed an invoice for a customer."""
        self.invoices.setdefault(customer_id, []).insert(0, invoice)

    def list_invoices(self, customer_id: str, *, limit: int = 20) -> list[dict]:
        return self.invoices.get(customer_id, [])[:limit]

    def verify_webhook(self, payload: bytes, signature: str, secret: str) -> WebhookEvent:
        if not hmac.compare_digest(signature, "valid"):
            raise WebhookVerificationError("invalid fake signature")
        try:
            event = json.loads(payload)
        except (ValueError, TypeError) as exc:
            raise WebhookVerificationError("payload is not valid JSON") from exc
        return WebhookEvent(type=event.get("type") or "", data=event.get("data") or {})


class StripePaymentProvider(PaymentProvider):
    """Real Stripe integration. Requires a configured API key."""

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("Stripe API key is required")
        import stripe

        self._stripe = stripe
        self._stripe.api_key = api_key

    def create_customer(self, email: str, *, metadata: dict | None = None) -> str:
        try:
            customer = self._stripe.Customer.create(email=email, metadata=metadata or {})
        except self._stripe.error.StripeError as exc:
            raise PaymentProviderError(f"create_customer failed: {exc}") from exc
        return customer.id

    def create_checkout_session(
        self, *, customer_id: str, price_id: str, success_url: str, cancel_url: str
    ) -> CheckoutSession:
        try:
            session = self._stripe.checkout.Session.create(
                customer=customer_id,
                mode="subscription",
                line_items=[{"price": price_id, "quantity": 1}],
                success_url=success_url,
                cancel_url=cancel_url,
            )
        except self._stripe.error.StripeError as exc:
            raise PaymentProviderError(f"create_checkout_session failed: {exc}") from exc
        return CheckoutSession(id=session.id, url=session.url)

    def create_billing_portal_session(self, *, customer_id: str, return_url: str) -> str:
        try:
            session = self._stripe.billing_portal.Session.create(
                customer=customer_id, return_url=return_url
            )
        except self._stripe.error.StripeError as exc:
            raise PaymentProviderError(f"create_billing_portal_session failed: {exc}") from exc
        return session.url

    def cancel_subscription(self, subscription_id: str, *, at_period_end: bool = True) -> None:
        try:
            if at_period_end:
                self._stripe.Subscription.modify(subscription_id, cancel_at_period_end=True)
            else:
                self._stripe.Subscription.delete(subscription_id)
        except self._stripe.error.StripeError as exc:
            raise PaymentProviderError(f"cancel_subscription failed: {exc}") from exc

    def list_invoices(self, customer_id: str, *, limit: int = 20) -> list[dict]:
        try:
            result = self._stripe.Invoice.list(customer=customer_id, limit=limit)
        except self._stripe.error.StripeError as exc:
            raise PaymentProviderError(f"list_invoices failed: {exc}") from exc
        return [
            {
                "id": inv.id,
                "amount_paid": inv.amount_paid,
                "currency": inv.currency,
                "status": inv.status,
                "created": inv.created,
                "hosted_invoice_url": getattr(inv, "hosted_invoice_url", None),
            }
            for inv in result.data
        ]

    def verify_webhook(self, payload: bytes, signature: str, secret: str) -> WebhookEvent:
        try:
            event = self._stripe.Webhook.construct_event(payload, signature, secret)
        except (ValueError, self._stripe.error.SignatureVerificationError) as exc:
            raise WebhookVerificationError(str(exc)) from exc
        return WebhookEvent(type=event["type"], data=event["data"])
