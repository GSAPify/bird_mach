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

    def verify_webhook(self, payload: bytes, signature: str, secret: str) -> WebhookEvent:
        if signature != "valid":
            raise WebhookVerificationError("invalid fake signature")
        try:
            event = json.loads(payload)
        except (ValueError, TypeError) as exc:
            raise WebhookVerificationError("payload is not valid JSON") from exc
        return WebhookEvent(type=event.get("type", ""), data=event.get("data", {}))


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

    def verify_webhook(self, payload: bytes, signature: str, secret: str) -> WebhookEvent:
        try:
            event = self._stripe.Webhook.construct_event(payload, signature, secret)
        except (ValueError, self._stripe.error.SignatureVerificationError) as exc:
            raise WebhookVerificationError(str(exc)) from exc
        return WebhookEvent(type=event["type"], data=event["data"])
