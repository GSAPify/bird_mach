"""End-to-end API tests for the auth router."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bird_mach.auth.audit import InMemoryAuditLog
from bird_mach.auth.dependencies import get_audit_log, get_auth_service
from bird_mach.auth.ratelimit import get_login_limiter
from bird_mach.auth.routes import router
from bird_mach.auth.service import AuthService
from bird_mach.auth.store import InMemoryUserRepository
from bird_mach.auth.tokens import TokenService
from bird_mach.rate_limiter import TokenBucketLimiter

SECRET = "routes-test-secret-at-least-32-bytes!!!"


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    service = AuthService(InMemoryUserRepository(), TokenService(SECRET))
    # get_current_user resolves the service via get_auth_service, so overriding
    # that one dependency is enough to bind the whole router to this instance.
    app.dependency_overrides[get_auth_service] = lambda: service
    # Generous limiter so rate limiting doesn't interfere with these cases;
    # the limiter itself is covered in test_ratelimit.py.
    app.dependency_overrides[get_login_limiter] = lambda: TokenBucketLimiter(
        capacity=1000, refill_rate=1000
    )
    audit = InMemoryAuditLog()
    app.dependency_overrides[get_audit_log] = lambda: audit
    return TestClient(app)


def _register_and_login(client, email="a@b.com", password="supersecret"):
    client.post("/auth/register", json={"email": email, "password": password})
    resp = client.post("/auth/login", json={"email": email, "password": password})
    return resp.json()


class TestRegister:
    def test_register_returns_201_and_no_secret(self, client):
        resp = client.post("/auth/register", json={"email": "a@b.com", "password": "supersecret"})
        assert resp.status_code == 201
        body = resp.json()
        assert body["email"] == "a@b.com"
        assert "password_hash" not in body

    def test_duplicate_returns_409(self, client):
        client.post("/auth/register", json={"email": "a@b.com", "password": "supersecret"})
        resp = client.post("/auth/register", json={"email": "a@b.com", "password": "supersecret"})
        assert resp.status_code == 409

    def test_short_password_returns_422(self, client):
        resp = client.post("/auth/register", json={"email": "a@b.com", "password": "x"})
        assert resp.status_code == 422


class TestLogin:
    def test_login_returns_tokens(self, client):
        tokens = _register_and_login(client)
        assert tokens["token_type"] == "bearer"
        assert tokens["access_token"] and tokens["refresh_token"]

    def test_wrong_password_returns_401(self, client):
        client.post("/auth/register", json={"email": "a@b.com", "password": "supersecret"})
        resp = client.post("/auth/login", json={"email": "a@b.com", "password": "nope12345"})
        assert resp.status_code == 401


class TestProtectedRoutes:
    def test_me_requires_token(self, client):
        assert client.get("/auth/me").status_code == 401

    def test_me_with_token(self, client):
        tokens = _register_and_login(client)
        resp = client.get("/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"})
        assert resp.status_code == 200
        assert resp.json()["email"] == "a@b.com"

    def test_refresh_flow(self, client):
        tokens = _register_and_login(client)
        resp = client.post("/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
        assert resp.status_code == 200
        assert resp.json()["access_token"]

    def test_change_password(self, client):
        tokens = _register_and_login(client)
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        resp = client.post(
            "/auth/change-password",
            json={"current_password": "supersecret", "new_password": "newsupersecret"},
            headers=headers,
        )
        assert resp.status_code == 204
        assert client.post(
            "/auth/login", json={"email": "a@b.com", "password": "newsupersecret"}
        ).status_code == 200

    def test_delete_account(self, client):
        tokens = _register_and_login(client)
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        assert client.delete("/auth/me", headers=headers).status_code == 204


class TestPasswordReset:
    def test_request_always_accepted(self, client):
        # Unknown email still returns 202 (no enumeration) with no token.
        resp = client.post("/auth/password-reset/request", json={"email": "ghost@x.com"})
        assert resp.status_code == 202
        assert "debug_reset_token" not in resp.json()

    def test_full_reset_flow(self, client):
        client.post("/auth/register", json={"email": "a@b.com", "password": "supersecret"})
        req = client.post("/auth/password-reset/request", json={"email": "a@b.com"})
        token = req.json()["debug_reset_token"]  # surfaced in non-prod

        resp = client.post(
            "/auth/password-reset/confirm",
            json={"token": token, "new_password": "brandnewsecret"},
        )
        assert resp.status_code == 204
        # New password works; old one no longer does.
        assert client.post(
            "/auth/login", json={"email": "a@b.com", "password": "brandnewsecret"}
        ).status_code == 200
        assert client.post(
            "/auth/login", json={"email": "a@b.com", "password": "supersecret"}
        ).status_code == 401

    def test_reset_token_single_use(self, client):
        client.post("/auth/register", json={"email": "a@b.com", "password": "supersecret"})
        token = client.post(
            "/auth/password-reset/request", json={"email": "a@b.com"}
        ).json()["debug_reset_token"]
        client.post(
            "/auth/password-reset/confirm",
            json={"token": token, "new_password": "brandnewsecret"},
        )
        # Reusing the same token after the password changed must fail.
        resp = client.post(
            "/auth/password-reset/confirm",
            json={"token": token, "new_password": "anothersecret1"},
        )
        assert resp.status_code == 400

    def test_invalid_token_rejected(self, client):
        resp = client.post(
            "/auth/password-reset/confirm",
            json={"token": "garbage", "new_password": "brandnewsecret"},
        )
        assert resp.status_code == 400


class TestAuditEvents:
    def test_login_recorded_in_events(self, client):
        tokens = _register_and_login(client)
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        events = client.get("/auth/events", headers=headers).json()["events"]
        kinds = {e["event_type"] for e in events}
        assert "registered" in kinds
        assert "login_success" in kinds

    def test_password_change_recorded(self, client):
        tokens = _register_and_login(client)
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        client.post(
            "/auth/change-password",
            json={"current_password": "supersecret", "new_password": "newsupersecret"},
            headers=headers,
        )
        events = client.get("/auth/events", headers=headers).json()["events"]
        assert "password_changed" in {e["event_type"] for e in events}
