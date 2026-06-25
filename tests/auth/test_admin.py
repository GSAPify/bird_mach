"""End-to-end tests for the admin user-management API."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from bird_mach.auth.admin import router
from bird_mach.auth.dependencies import get_auth_service
from bird_mach.auth.models import Role
from bird_mach.auth.service import AuthService
from bird_mach.auth.store import InMemoryUserRepository
from bird_mach.auth.tokens import TokenService

SECRET = "admin-routes-secret-at-least-32-bytes!!!"


@pytest.fixture
def ctx():
    repo = InMemoryUserRepository()
    service = AuthService(repo, TokenService(SECRET))
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_auth_service] = lambda: service
    client = TestClient(app)

    admin = service.register("admin@x.com", "supersecret", role=Role.ADMIN)
    member = service.register("user@x.com", "supersecret")
    admin_tok = service.login("admin@x.com", "supersecret").access_token
    user_tok = service.login("user@x.com", "supersecret").access_token
    return client, service, admin, member, admin_tok, user_tok


def _h(token):
    return {"Authorization": f"Bearer {token}"}


class TestAuthorization:
    def test_non_admin_forbidden(self, ctx):
        client, _, _, _, _, user_tok = ctx
        assert client.get("/auth/admin/users", headers=_h(user_tok)).status_code == 403

    def test_anonymous_unauthorized(self, ctx):
        client, *_ = ctx
        assert client.get("/auth/admin/users").status_code == 401

    def test_admin_allowed(self, ctx):
        client, _, _, _, admin_tok, _ = ctx
        resp = client.get("/auth/admin/users", headers=_h(admin_tok))
        assert resp.status_code == 200
        assert len(resp.json()["users"]) == 2


class TestUserManagement:
    def test_get_user(self, ctx):
        client, _, _, member, admin_tok, _ = ctx
        resp = client.get(f"/auth/admin/users/{member.id}", headers=_h(admin_tok))
        assert resp.status_code == 200
        assert resp.json()["email"] == "user@x.com"

    def test_get_missing_user_404(self, ctx):
        client, _, _, _, admin_tok, _ = ctx
        assert client.get("/auth/admin/users/ghost", headers=_h(admin_tok)).status_code == 404

    def test_deactivate_and_reactivate(self, ctx):
        client, service, _, member, admin_tok, _ = ctx
        resp = client.post(f"/auth/admin/users/{member.id}/deactivate", headers=_h(admin_tok))
        assert resp.status_code == 200
        assert resp.json()["is_active"] is False
        resp = client.post(f"/auth/admin/users/{member.id}/activate", headers=_h(admin_tok))
        assert resp.json()["is_active"] is True

    def test_set_role(self, ctx):
        client, service, _, member, admin_tok, _ = ctx
        resp = client.put(
            f"/auth/admin/users/{member.id}/role",
            json={"role": "admin"},
            headers=_h(admin_tok),
        )
        assert resp.status_code == 200
        assert resp.json()["role"] == "admin"
        assert service.get_user(member.id).role is Role.ADMIN
