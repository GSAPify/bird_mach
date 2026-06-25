"""Tests for JWT issuance and verification."""

from __future__ import annotations

import time

import jwt
import pytest

from bird_mach.auth.tokens import ACCESS_TOKEN, REFRESH_TOKEN, TokenService
from bird_mach.exceptions import TokenError

SECRET = "test-secret-that-is-at-least-32-bytes-long"


@pytest.fixture
def svc():
    return TokenService(SECRET)


class TestTokenService:
    def test_rejects_weak_secret(self):
        with pytest.raises(ValueError):
            TokenService("short")

    def test_access_token_roundtrip(self, svc):
        token = svc.issue_access("user-1", "user")
        claims = svc.verify(token)
        assert claims.subject == "user-1"
        assert claims.role == "user"
        assert claims.token_type == ACCESS_TOKEN

    def test_refresh_token_roundtrip(self, svc):
        token = svc.issue_refresh("user-1", "admin")
        claims = svc.verify(token, expected_type=REFRESH_TOKEN)
        assert claims.role == "admin"

    def test_refresh_cannot_be_used_as_access(self, svc):
        refresh = svc.issue_refresh("user-1", "user")
        with pytest.raises(TokenError):
            svc.verify(refresh, expected_type=ACCESS_TOKEN)

    def test_tampered_signature_rejected(self, svc):
        token = svc.issue_access("user-1", "user")
        forged = token[:-3] + ("aaa" if not token.endswith("aaa") else "bbb")
        with pytest.raises(TokenError):
            svc.verify(forged)

    def test_wrong_secret_rejected(self, svc):
        token = svc.issue_access("user-1", "user")
        other = TokenService("a-totally-different-secret-value-32b!!")
        with pytest.raises(TokenError):
            other.verify(token)

    def test_expired_token_rejected(self):
        svc = TokenService(SECRET, access_ttl_s=1)
        token = svc.issue_access("user-1", "user")
        time.sleep(1.2)
        with pytest.raises(TokenError):
            svc.verify(token)

    def test_password_reset_roundtrip(self, svc):
        token = svc.issue_password_reset("user-1", "hash-v1")
        assert svc.verify_password_reset(token, "hash-v1") == "user-1"
        assert svc.password_reset_subject(token) == "user-1"

    def test_password_reset_invalidated_when_hash_changes(self, svc):
        token = svc.issue_password_reset("user-1", "hash-v1")
        # After the password (hash) changes, the old reset token is dead.
        with pytest.raises(TokenError):
            svc.verify_password_reset(token, "hash-v2")

    def test_access_token_not_accepted_as_reset(self, svc):
        access = svc.issue_access("user-1", "user")
        with pytest.raises(TokenError):
            svc.password_reset_subject(access)

    def test_foreign_issuer_rejected(self, svc):
        token = jwt.encode(
            {"sub": "x", "iss": "evil", "type": "access", "exp": 9_999_999_999},
            SECRET,
            algorithm="HS256",
        )
        with pytest.raises(TokenError):
            svc.verify(token)
