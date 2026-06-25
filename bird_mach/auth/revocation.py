"""Refresh-token revocation (logout) via a token-id denylist.

JWTs are stateless and can't be invalidated before they expire, so logging out
a refresh token means recording its ``jti`` in a denylist that the refresh path
consults. Entries carry the token's own expiry so the denylist can be pruned —
once the token would have expired anyway, the entry is dead weight.

SQLite-backed by default; in-memory for tests.
"""

from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from datetime import datetime, timezone

from bird_mach.db import Database

_SCHEMA = """
CREATE TABLE IF NOT EXISTS revoked_tokens (
    jti        TEXT PRIMARY KEY,
    expires_at TEXT NOT NULL
);
"""


class RevokedTokenStore(ABC):
    @abstractmethod
    def revoke(self, jti: str, expires_at: datetime) -> None: ...

    @abstractmethod
    def is_revoked(self, jti: str) -> bool: ...

    @abstractmethod
    def purge_expired(self, *, now: datetime | None = None) -> int:
        """Drop entries already past expiry; return how many were removed."""


class InMemoryRevokedTokenStore(RevokedTokenStore):
    def __init__(self) -> None:
        self._revoked: dict[str, datetime] = {}
        self._lock = threading.RLock()

    def revoke(self, jti: str, expires_at: datetime) -> None:
        if not jti:
            return
        with self._lock:
            self._revoked[jti] = expires_at

    def is_revoked(self, jti: str) -> bool:
        return bool(jti) and jti in self._revoked

    def purge_expired(self, *, now: datetime | None = None) -> int:
        cutoff = now or datetime.now(timezone.utc)
        with self._lock:
            stale = [j for j, exp in self._revoked.items() if exp <= cutoff]
            for j in stale:
                del self._revoked[j]
            return len(stale)


class SqliteRevokedTokenStore(RevokedTokenStore):
    def __init__(self, db: Database) -> None:
        self._db = db
        self._db.executescript(_SCHEMA)

    def revoke(self, jti: str, expires_at: datetime) -> None:
        if not jti:
            return
        self._db.execute(
            "INSERT INTO revoked_tokens (jti, expires_at) VALUES (?, ?) "
            "ON CONFLICT(jti) DO NOTHING",
            [jti, expires_at.isoformat()],
        )

    def is_revoked(self, jti: str) -> bool:
        if not jti:
            return False
        return self._db.query_one("SELECT 1 FROM revoked_tokens WHERE jti = ?", [jti]) is not None

    def purge_expired(self, *, now: datetime | None = None) -> int:
        cutoff = (now or datetime.now(timezone.utc)).isoformat()
        cur = self._db.execute("DELETE FROM revoked_tokens WHERE expires_at <= ?", [cutoff])
        return cur.rowcount
