"""Verify the security-headers middleware on the real application."""

from __future__ import annotations

from fastapi.testclient import TestClient

from bird_mach.webapp import app

client = TestClient(app)


def test_security_headers_present_on_responses():
    resp = client.get("/health")
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert resp.headers["X-Frame-Options"] == "DENY"
    assert resp.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"


def test_security_headers_present_on_404():
    # Middleware runs for every response, including error responses.
    resp = client.get("/does-not-exist")
    assert resp.status_code == 404
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
