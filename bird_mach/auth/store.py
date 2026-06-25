"""User persistence: a storage-agnostic repository with two backends.

``InMemoryUserRepository`` is for tests and ephemeral use; ``SqliteUserRepository``
is the durable default for deployments. Both implement the same
:class:`UserRepository` protocol so the service layer never knows which is in
play, and a future Postgres backend only needs to satisfy the same interface.
"""

from __future__ import annotations

import sqlite3
import threading
from abc import ABC, abstractmethod
from datetime import datetime

from bird_mach.auth.models import Role, User
from bird_mach.db import Database

_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id                 TEXT PRIMARY KEY,
    email              TEXT NOT NULL UNIQUE,
    password_hash      TEXT NOT NULL,
    role               TEXT NOT NULL DEFAULT 'user',
    is_active          INTEGER NOT NULL DEFAULT 1,
    created_at         TEXT NOT NULL,
    stripe_customer_id TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users (email);
"""


def _normalise_email(email: str) -> str:
    return email.strip().lower()


class UserRepository(ABC):
    """Storage interface for user accounts. Emails are matched case-insensitively."""

    @abstractmethod
    def add(self, user: User) -> User: ...

    @abstractmethod
    def get(self, user_id: str) -> User | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def get_by_stripe_customer_id(self, customer_id: str) -> User | None: ...

    @abstractmethod
    def update(self, user: User) -> User: ...

    @abstractmethod
    def delete(self, user_id: str) -> bool: ...

    @abstractmethod
    def count(self) -> int: ...

    @abstractmethod
    def list_all(self, *, limit: int = 100, offset: int = 0) -> list[User]:
        """Return users ordered by creation time (oldest first), for admin views."""


class InMemoryUserRepository(UserRepository):
    """Thread-safe dict-backed repository for tests and ephemeral runs."""

    def __init__(self) -> None:
        self._by_id: dict[str, User] = {}
        self._lock = threading.RLock()

    def add(self, user: User) -> User:
        with self._lock:
            if self.get_by_email(user.email) is not None:
                raise ValueError(f"email already exists: {user.email}")
            self._by_id[user.id] = user
            return user

    def get(self, user_id: str) -> User | None:
        return self._by_id.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        target = _normalise_email(email)
        return next(
            (u for u in self._by_id.values() if _normalise_email(u.email) == target),
            None,
        )

    def get_by_stripe_customer_id(self, customer_id: str) -> User | None:
        return next(
            (u for u in self._by_id.values() if u.stripe_customer_id == customer_id),
            None,
        )

    def update(self, user: User) -> User:
        with self._lock:
            if user.id not in self._by_id:
                raise KeyError(user.id)
            self._by_id[user.id] = user
            return user

    def delete(self, user_id: str) -> bool:
        with self._lock:
            return self._by_id.pop(user_id, None) is not None

    def count(self) -> int:
        return len(self._by_id)

    def list_all(self, *, limit: int = 100, offset: int = 0) -> list[User]:
        ordered = sorted(self._by_id.values(), key=lambda u: u.created_at)
        return ordered[offset : offset + limit]


class SqliteUserRepository(UserRepository):
    """Durable repository backed by :class:`bird_mach.db.Database`."""

    def __init__(self, db: Database) -> None:
        self._db = db
        self._db.executescript(_SCHEMA)

    @staticmethod
    def _row_to_user(row) -> User:
        return User(
            id=row["id"],
            email=row["email"],
            password_hash=row["password_hash"],
            role=Role(row["role"]),
            is_active=bool(row["is_active"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            stripe_customer_id=row["stripe_customer_id"],
        )

    def add(self, user: User) -> User:
        try:
            self._db.execute(
                "INSERT INTO users (id, email, password_hash, role, is_active, "
                "created_at, stripe_customer_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                [
                    user.id,
                    _normalise_email(user.email),
                    user.password_hash,
                    user.role.value,
                    int(user.is_active),
                    user.created_at.isoformat(),
                    user.stripe_customer_id,
                ],
            )
        except sqlite3.IntegrityError as exc:
            raise ValueError(f"email already exists: {user.email}") from exc
        return user

    def get(self, user_id: str) -> User | None:
        row = self._db.query_one("SELECT * FROM users WHERE id = ?", [user_id])
        return self._row_to_user(row) if row else None

    def get_by_email(self, email: str) -> User | None:
        row = self._db.query_one(
            "SELECT * FROM users WHERE email = ?", [_normalise_email(email)]
        )
        return self._row_to_user(row) if row else None

    def get_by_stripe_customer_id(self, customer_id: str) -> User | None:
        row = self._db.query_one(
            "SELECT * FROM users WHERE stripe_customer_id = ?", [customer_id]
        )
        return self._row_to_user(row) if row else None

    def update(self, user: User) -> User:
        cur = self._db.execute(
            "UPDATE users SET email = ?, password_hash = ?, role = ?, is_active = ?, "
            "stripe_customer_id = ? WHERE id = ?",
            [
                _normalise_email(user.email),
                user.password_hash,
                user.role.value,
                int(user.is_active),
                user.stripe_customer_id,
                user.id,
            ],
        )
        if cur.rowcount == 0:
            raise KeyError(user.id)
        return user

    def delete(self, user_id: str) -> bool:
        cur = self._db.execute("DELETE FROM users WHERE id = ?", [user_id])
        return cur.rowcount > 0

    def count(self) -> int:
        return self._db.query_one("SELECT COUNT(*) AS c FROM users")["c"]

    def list_all(self, *, limit: int = 100, offset: int = 0) -> list[User]:
        rows = self._db.query_all(
            "SELECT * FROM users ORDER BY created_at ASC LIMIT ? OFFSET ?",
            [limit, offset],
        )
        return [self._row_to_user(r) for r in rows]
