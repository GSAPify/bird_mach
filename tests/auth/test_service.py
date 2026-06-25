"""Tests for the authentication service."""

from __future__ import annotations

import pytest

from bird_mach.auth.models import Role
from bird_mach.auth.service import AuthService
from bird_mach.auth.store import InMemoryUserRepository
from bird_mach.auth.tokens import ACCESS_TOKEN, REFRESH_TOKEN, TokenService
from bird_mach.exceptions import (
    EmailAlreadyRegisteredError,
    InactiveUserError,
    InvalidCredentialsError,
    UserNotFoundError,
)

SECRET = "service-test-secret-at-least-32-bytes!!"


@pytest.fixture
def svc():
    return AuthService(InMemoryUserRepository(), TokenService(SECRET))


class TestRegister:
    def test_register_creates_active_user(self, svc):
        user = svc.register("New@Example.com", "supersecret")
        assert user.email == "new@example.com"  # normalised
        assert user.is_active
        assert user.role is Role.USER

    def test_duplicate_email_rejected(self, svc):
        svc.register("dup@example.com", "supersecret")
        with pytest.raises(EmailAlreadyRegisteredError):
            svc.register("DUP@example.com", "anothersecret")

    def test_invalid_email_rejected(self, svc):
        with pytest.raises(ValueError):
            svc.register("not-an-email", "supersecret")

    def test_short_password_rejected(self, svc):
        with pytest.raises(ValueError):
            svc.register("a@b.com", "short")

    def test_all_numeric_password_rejected(self, svc):
        with pytest.raises(ValueError):
            svc.register("a@b.com", "12345678")

    def test_single_repeated_char_password_rejected(self, svc):
        with pytest.raises(ValueError):
            svc.register("a@b.com", "aaaaaaaa")


class TestLogin:
    def test_login_returns_token_pair(self, svc):
        svc.register("a@b.com", "supersecret")
        pair = svc.login("a@b.com", "supersecret")
        claims = svc._tokens.verify(pair.access_token, expected_type=ACCESS_TOKEN)
        assert claims.role == "user"
        svc._tokens.verify(pair.refresh_token, expected_type=REFRESH_TOKEN)

    def test_wrong_password_rejected(self, svc):
        svc.register("a@b.com", "supersecret")
        with pytest.raises(InvalidCredentialsError):
            svc.login("a@b.com", "wrongpass")

    def test_unknown_email_same_error_as_wrong_password(self, svc):
        # No user enumeration: unknown email raises the same error type.
        with pytest.raises(InvalidCredentialsError):
            svc.login("ghost@b.com", "whatever1")

    def test_inactive_user_cannot_login(self, svc):
        user = svc.register("a@b.com", "supersecret")
        svc.deactivate(user.id)
        with pytest.raises(InactiveUserError):
            svc.login("a@b.com", "supersecret")


class TestRefresh:
    def test_refresh_issues_new_pair(self, svc):
        svc.register("a@b.com", "supersecret")
        pair = svc.login("a@b.com", "supersecret")
        new_pair = svc.refresh(pair.refresh_token)
        svc._tokens.verify(new_pair.access_token, expected_type=ACCESS_TOKEN)

    def test_access_token_rejected_as_refresh(self, svc):
        svc.register("a@b.com", "supersecret")
        pair = svc.login("a@b.com", "supersecret")
        from bird_mach.exceptions import TokenError

        with pytest.raises(TokenError):
            svc.refresh(pair.access_token)

    def test_logout_revokes_refresh_token(self, svc):
        from bird_mach.exceptions import TokenError

        svc.register("a@b.com", "supersecret")
        pair = svc.login("a@b.com", "supersecret")
        # Works before logout.
        svc.refresh(pair.refresh_token)
        svc.logout(pair.refresh_token)
        with pytest.raises(TokenError):
            svc.refresh(pair.refresh_token)

    def test_logout_does_not_affect_other_tokens(self, svc):
        svc.register("a@b.com", "supersecret")
        pair1 = svc.login("a@b.com", "supersecret")
        pair2 = svc.login("a@b.com", "supersecret")
        svc.logout(pair1.refresh_token)
        # The second session's refresh token still works.
        assert svc.refresh(pair2.refresh_token).access_token


class TestAccountManagement:
    def test_change_password(self, svc):
        user = svc.register("a@b.com", "supersecret")
        svc.change_password(user.id, "supersecret", "newsupersecret")
        svc.login("a@b.com", "newsupersecret")
        with pytest.raises(InvalidCredentialsError):
            svc.login("a@b.com", "supersecret")

    def test_change_password_wrong_current_rejected(self, svc):
        user = svc.register("a@b.com", "supersecret")
        with pytest.raises(InvalidCredentialsError):
            svc.change_password(user.id, "wrong", "newsupersecret")

    def test_delete(self, svc):
        user = svc.register("a@b.com", "supersecret")
        svc.delete(user.id)
        with pytest.raises(UserNotFoundError):
            svc.delete(user.id)
