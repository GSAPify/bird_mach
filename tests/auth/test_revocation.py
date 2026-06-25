"""Tests for the refresh-token revocation denylist."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from bird_mach.auth.revocation import (
    InMemoryRevokedTokenStore,
    SqliteRevokedTokenStore,
)
from bird_mach.db import Database


@pytest.fixture(params=["memory", "sqlite"])
def store(request):
    if request.param == "memory":
        return InMemoryRevokedTokenStore()
    return SqliteRevokedTokenStore(Database(":memory:"))


def _future() -> datetime:
    return datetime.now(timezone.utc) + timedelta(hours=1)


class TestRevocation:
    def test_revoke_and_check(self, store):
        assert store.is_revoked("jti-1") is False
        store.revoke("jti-1", _future())
        assert store.is_revoked("jti-1") is True

    def test_empty_jti_is_noop(self, store):
        store.revoke("", _future())
        assert store.is_revoked("") is False

    def test_revoke_is_idempotent(self, store):
        store.revoke("jti-1", _future())
        store.revoke("jti-1", _future())
        assert store.is_revoked("jti-1") is True

    def test_purge_expired_removes_only_stale(self, store):
        past = datetime.now(timezone.utc) - timedelta(hours=1)
        store.revoke("stale", past)
        store.revoke("fresh", _future())
        removed = store.purge_expired()
        assert removed == 1
        assert store.is_revoked("stale") is False
        assert store.is_revoked("fresh") is True
