"""Tests for the user repositories.

Both backends are exercised through the same cases so the in-memory test
double cannot drift from the durable SQLite implementation.
"""

from __future__ import annotations

import pytest

from bird_mach.auth.models import Role, User
from bird_mach.auth.store import (
    InMemoryUserRepository,
    SqliteUserRepository,
)
from bird_mach.db import Database


@pytest.fixture(params=["memory", "sqlite"])
def repo(request):
    if request.param == "memory":
        return InMemoryUserRepository()
    return SqliteUserRepository(Database(":memory:"))


def _user(uid="u1", email="alice@example.com") -> User:
    return User(id=uid, email=email, password_hash="hash", role=Role.USER)


class TestUserRepository:
    def test_add_and_get(self, repo):
        repo.add(_user())
        fetched = repo.get("u1")
        assert fetched is not None
        assert fetched.email == "alice@example.com"

    def test_get_by_email_is_case_insensitive(self, repo):
        repo.add(_user(email="Alice@Example.com"))
        assert repo.get_by_email("alice@example.com") is not None
        assert repo.get_by_email("ALICE@EXAMPLE.COM") is not None

    def test_duplicate_email_rejected(self, repo):
        repo.add(_user(uid="u1", email="dup@example.com"))
        with pytest.raises(ValueError):
            repo.add(_user(uid="u2", email="dup@example.com"))

    def test_get_missing_returns_none(self, repo):
        assert repo.get("nope") is None
        assert repo.get_by_email("nobody@example.com") is None

    def test_update(self, repo):
        repo.add(_user())
        u = repo.get("u1")
        u.role = Role.ADMIN
        u.stripe_customer_id = "cus_123"
        repo.update(u)
        refreshed = repo.get("u1")
        assert refreshed.role == Role.ADMIN
        assert refreshed.stripe_customer_id == "cus_123"

    def test_update_unknown_raises(self, repo):
        with pytest.raises(KeyError):
            repo.update(_user(uid="ghost"))

    def test_delete(self, repo):
        repo.add(_user())
        assert repo.delete("u1") is True
        assert repo.get("u1") is None
        assert repo.delete("u1") is False

    def test_get_by_stripe_customer_id(self, repo):
        u = _user()
        u.stripe_customer_id = "cus_abc"
        repo.add(u)
        assert repo.get_by_stripe_customer_id("cus_abc").id == "u1"
        assert repo.get_by_stripe_customer_id("cus_missing") is None

    def test_count(self, repo):
        assert repo.count() == 0
        repo.add(_user(uid="a", email="a@x.com"))
        repo.add(_user(uid="b", email="b@x.com"))
        assert repo.count() == 2


def test_sqlite_repository_persists_across_handles(tmp_path):
    db = Database(tmp_path / "users.db")
    SqliteUserRepository(db).add(_user())
    db.close()

    reopened = SqliteUserRepository(Database(tmp_path / "users.db"))
    assert reopened.get_by_email("alice@example.com") is not None
