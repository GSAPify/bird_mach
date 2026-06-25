"""End-to-end API tests for the auth router."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bird_mach.auth.dependencies import get_auth_service
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
