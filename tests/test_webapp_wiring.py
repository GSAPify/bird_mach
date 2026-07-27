"""Smoke tests that the app factory wires in auth and billing."""

from __future__ import annotations

from fastapi.testclient import TestClient

from bird_mach.webapp import app

client = TestClient(app)


def registered_paths(routes):
    """Collect every registered route path, tolerating both route layouts.

    FastAPI < 0.140 flattens ``include_router`` calls into ``app.routes`` as
    plain routes carrying ``.path``. Newer versions insert a private
    ``_IncludedRouter`` wrapper that has no ``.path`` and defers to
    ``.original_router``. Walk both so this test does not pin the repo to one
    FastAPI/Starlette release.
    """
    paths = set()
    for route in routes:
        path = getattr(route, "path", None)
        if path is not None:
            paths.add(path)
        nested = getattr(route, "routes", None)
        if nested:
            paths |= registered_paths(nested)
        included = getattr(route, "original_router", None)
        if included is not None:
            paths |= registered_paths(included.routes)
    return paths


def test_health_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_auth_routes_registered():
    paths = registered_paths(app.routes)
    assert "/auth/login" in paths
    assert "/auth/register" in paths


def test_billing_routes_registered():
    paths = registered_paths(app.routes)
    assert "/billing/plans" in paths
    assert "/billing/webhook" in paths


def test_plans_endpoint_serves():
    resp = client.get("/billing/plans")
    assert resp.status_code == 200
    assert "plans" in resp.json()


def test_protected_route_requires_auth():
    assert client.get("/auth/me").status_code == 401


def test_api_v1_router_mounted():
    paths = registered_paths(app.routes)
    assert "/api/v1/analyze" in paths
    assert "/api/v1/health" in paths


def test_readiness_probe_checks_database():
    resp = client.get("/health/ready")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ready", "database": "ok"}
