"""Durable audit log for security-relevant auth events.

Records who did what and when (login success/failure, registration, password
change, account deletion) so operators can investigate suspicious activity.
Stored durably because an audit trail that evaporates on restart is no audit
trail. SQLite-backed by default, in-memory for tests.
"""

from __future__ import annotations

import enum
import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from bird_mach.db import Database


class AuthEventType(str, enum.Enum):
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    REGISTERED = "registered"
    PASSWORD_CHANGED = "password_changed"
    ACCOUNT_DELETED = "account_deleted"


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class AuthEvent:
    event_type: AuthEventType
    # user_id is None for failures where the account couldn't be resolved.
    user_id: str | None = None
    email: str | None = None
    ip: str | None = None
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    created_at: datetime = field(default_factory=_now)

    def public_dict(self) -> dict:
        return {
            "id": self.id,
            "event_type": self.event_type.value,
            "user_id": self.user_id,
            "email": self.email,
            "ip": self.ip,
            "created_at": self.created_at.isoformat(),
        }


_SCHEMA = """
CREATE TABLE IF NOT EXISTS auth_events (
    id         TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    user_id    TEXT,
    email      TEXT,
    ip         TEXT,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_auth_events_user ON auth_events (user_id);
CREATE INDEX IF NOT EXISTS idx_auth_events_created ON auth_events (created_at);
"""


class AuditLog:
    """Append-only audit log. Two backends share this interface via duck typing."""

    def record(self, event: AuthEvent) -> AuthEvent:  # pragma: no cover - overridden
        raise NotImplementedError

    def recent_for_user(self, user_id: str, *, limit: int = 50) -> list[AuthEvent]:
        raise NotImplementedError  # pragma: no cover - overridden


class InMemoryAuditLog(AuditLog):
    def __init__(self) -> None:
        self._events: list[AuthEvent] = []
        self._lock = threading.RLock()

    def record(self, event: AuthEvent) -> AuthEvent:
        with self._lock:
            self._events.append(event)
            return event

    def recent_for_user(self, user_id: str, *, limit: int = 50) -> list[AuthEvent]:
        matches = [e for e in self._events if e.user_id == user_id]
        return sorted(matches, key=lambda e: e.created_at, reverse=True)[:limit]


class SqliteAuditLog(AuditLog):
    def __init__(self, db: Database) -> None:
        self._db = db
        self._db.executescript(_SCHEMA)

    def record(self, event: AuthEvent) -> AuthEvent:
        self._db.execute(
            "INSERT INTO auth_events (id, event_type, user_id, email, ip, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            [
                event.id,
                event.event_type.value,
                event.user_id,
                event.email,
                event.ip,
                event.created_at.isoformat(),
            ],
        )
        return event

    def recent_for_user(self, user_id: str, *, limit: int = 50) -> list[AuthEvent]:
        rows = self._db.query_all(
            "SELECT * FROM auth_events WHERE user_id = ? "
            "ORDER BY created_at DESC LIMIT ?",
            [user_id, limit],
        )
        return [
            AuthEvent(
                id=r["id"],
                event_type=AuthEventType(r["event_type"]),
                user_id=r["user_id"],
                email=r["email"],
                ip=r["ip"],
                created_at=datetime.fromisoformat(r["created_at"]),
            )
            for r in rows
        ]
