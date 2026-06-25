"""Smoke tests that the app factory wires in auth and billing."""

from __future__ import annotations

from fastapi.testclient import TestClient

from bird_mach.webapp import app

client = TestClient(app)


def test_health_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_auth_routes_registered():
    paths = {route.path for route in app.routes}
    assert "/auth/login" in paths
    assert "/auth/register" in paths


def test_billing_routes_registered():
    paths = {route.path for route in app.routes}
    assert "/billing/plans" in paths
    assert "/billing/webhook" in paths


def test_plans_endpoint_serves():
    resp = client.get("/billing/plans")
    assert resp.status_code == 200
    assert "plans" in resp.json()


def test_protected_route_requires_auth():
    assert client.get("/auth/me").status_code == 401
