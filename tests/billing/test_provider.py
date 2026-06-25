"""Tests for the fake payment provider (real Stripe path is integration-only)."""

from __future__ import annotations

import json

import pytest

from bird_mach.billing.provider import FakePaymentProvider
from bird_mach.exceptions import WebhookVerificationError


@pytest.fixture
def provider():
    return FakePaymentProvider()


class TestFakeProvider:
    def test_create_customer_records_call(self, provider):
        cid = provider.create_customer("a@b.com", metadata={"user_id": "u1"})
        assert cid.startswith("cus_fake_")
        assert provider.customers[0]["email"] == "a@b.com"
        assert provider.customers[0]["metadata"] == {"user_id": "u1"}

    def test_checkout_session_has_url(self, provider):
        session = provider.create_checkout_session(
            customer_id="cus_1",
            price_id="price_1",
            success_url="https://x/ok",
            cancel_url="https://x/no",
        )
        assert session.id.startswith("cs_fake_")
        assert session.url.endswith(session.id)

    def test_portal_session(self, provider):
        url = provider.create_billing_portal_session(
            customer_id="cus_1", return_url="https://x/back"
        )
        assert url.startswith("https://fake.stripe/portal/")

    def test_webhook_valid_signature(self, provider):
        payload = json.dumps(
            {"type": "customer.subscription.updated", "data": {"object": {"id": "sub_1"}}}
        ).encode()
        event = provider.verify_webhook(payload, "valid", "whsec_x")
        assert event.type == "customer.subscription.updated"
        assert event.data["object"]["id"] == "sub_1"

    def test_webhook_bad_signature_rejected(self, provider):
        with pytest.raises(WebhookVerificationError):
            provider.verify_webhook(b"{}", "wrong", "whsec_x")

    def test_webhook_bad_payload_rejected(self, provider):
        with pytest.raises(WebhookVerificationError):
            provider.verify_webhook(b"not json", "valid", "whsec_x")

    def test_cancel_subscription_records_call(self, provider):
        provider.cancel_subscription("sub_1", at_period_end=True)
        assert provider.cancellations == [{"id": "sub_1", "at_period_end": True}]
