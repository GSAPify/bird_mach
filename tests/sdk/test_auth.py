"""Tests for SDK authentication."""
from bird_mach.sdk.auth import APIKeyAuth, HMACAuth

class TestAPIKeyAuth:
    def test_headers(self):
        auth = APIKeyAuth("sk-test-123")
        h = auth.headers()
        assert h["Authorization"] == "Bearer sk-test-123"

    def test_not_configured(self):
        assert not APIKeyAuth("").is_configured

    def test_configured(self):
        assert APIKeyAuth("key").is_configured

class TestHMACAuth:
    def test_sign(self):
        auth = HMACAuth("key-1", "secret")
        headers = auth.sign('{"data": 1}')
        assert "X-Key-Id" in headers
        assert "X-Signature" in headers
        assert len(headers["X-Signature"]) == 64
