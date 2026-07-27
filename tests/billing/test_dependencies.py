"""Tests for billing dependency wiring."""

from __future__ import annotations

import pytest

from bird_mach.billing.dependencies import _build_provider
from bird_mach.billing.provider import FakePaymentProvider
from bird_mach.config import AppConfig


class TestBuildProvider:
    def test_production_without_stripe_key_raises(self):
        """The fake accepts a webhook signed "valid"; never serve it in prod."""
        config = AppConfig(environment="production", stripe_api_key="")
        with pytest.raises(RuntimeError, match="STRIPE_API_KEY"):
            _build_provider(config)

    def test_non_production_without_stripe_key_uses_fake(self):
        config = AppConfig(environment="development", stripe_api_key="")
        assert isinstance(_build_provider(config), FakePaymentProvider)
