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

    def test_list_all_paginates(self, repo):
        for i in range(5):
            repo.add(_user(uid=f"u{i}", email=f"u{i}@x.com"))
        assert len(repo.list_all(limit=2)) == 2
        assert len(repo.list_all(limit=2, offset=4)) == 1
        all_ids = {u.id for u in repo.list_all()}
        assert all_ids == {f"u{i}" for i in range(5)}


def test_sqlite_repository_persists_across_handles(tmp_path):
    db = Database(tmp_path / "users.db")
    SqliteUserRepository(db).add(_user())
    db.close()

    reopened = SqliteUserRepository(Database(tmp_path / "users.db"))
    assert reopened.get_by_email("alice@example.com") is not None


def test_is_verified_roundtrips(repo):
    u = _user()
    u.is_verified = True
    repo.add(u)
    assert repo.get("u1").is_verified is True


def test_migration_adds_is_verified_to_old_schema(tmp_path):
    # Simulate a DB created before is_verified existed.
    db = Database(tmp_path / "old.db")
    db.executescript(
        """
        CREATE TABLE users (
            id TEXT PRIMARY KEY, email TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user', is_active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL, stripe_customer_id TEXT
        );
        """
    )
    db.execute(
        "INSERT INTO users (id, email, password_hash, role, is_active, created_at) "
        "VALUES ('u1', 'a@b.com', 'h', 'user', 1, '2026-01-01T00:00:00+00:00')"
    )
    # Opening the repository should ALTER the table and read the legacy row.
    repo = SqliteUserRepository(db)
    user = repo.get("u1")
    assert user is not None
    assert user.is_verified is False
