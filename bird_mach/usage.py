"""Per-user usage metering for free-tier quota enforcement.

Free accounts get a capped number of analyses per UTC day; subscribers are
unlimited. Counts are durable (a restart must not reset someone's daily usage
to zero and hand them a fresh quota), so this uses the SQLite layer with an
in-memory backend for tests.
"""

from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from datetime import datetime, timezone

from bird_mach.db import Database

# Mirrors the "Up to 5 analyses per day" promise in the free plan catalog entry.
FREE_DAILY_ANALYSES = 5

_SCHEMA = """
CREATE TABLE IF NOT EXISTS usage_daily (
    user_id  TEXT NOT NULL,
    day      TEXT NOT NULL,
    count    INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, day)
);
"""


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


class UsageRepository(ABC):
    @abstractmethod
    def increment(self, user_id: str, day: str) -> int:
        """Add one to the user's count for ``day`` and return the new total."""

    @abstractmethod
    def count(self, user_id: str, day: str) -> int: ...


class InMemoryUsageRepository(UsageRepository):
    def __init__(self) -> None:
        self._counts: dict[tuple[str, str], int] = {}
        self._lock = threading.RLock()

    def increment(self, user_id: str, day: str) -> int:
        with self._lock:
            new = self._counts.get((user_id, day), 0) + 1
            self._counts[(user_id, day)] = new
            return new

    def count(self, user_id: str, day: str) -> int:
        return self._counts.get((user_id, day), 0)


class SqliteUsageRepository(UsageRepository):
    def __init__(self, db: Database) -> None:
        self._db = db
        self._db.executescript(_SCHEMA)

    def increment(self, user_id: str, day: str) -> int:
        self._db.execute(
            "INSERT INTO usage_daily (user_id, day, count) VALUES (?, ?, 1) "
            "ON CONFLICT(user_id, day) DO UPDATE SET count = count + 1",
            [user_id, day],
        )
        return self.count(user_id, day)

    def count(self, user_id: str, day: str) -> int:
        row = self._db.query_one(
            "SELECT count FROM usage_daily WHERE user_id = ? AND day = ?",
            [user_id, day],
        )
        return row["count"] if row else 0


class UsageService:
    def __init__(self, repo: UsageRepository, *, free_daily_limit: int = FREE_DAILY_ANALYSES):
        self._repo = repo
        self._limit = free_daily_limit

    @property
    def free_daily_limit(self) -> int:
        return self._limit

    def used_today(self, user_id: str, *, day: str | None = None) -> int:
        return self._repo.count(user_id, day or _today())

    def record(self, user_id: str, *, day: str | None = None) -> int:
        """Record one analysis and return the new daily total."""
        return self._repo.increment(user_id, day or _today())

    def free_tier_exhausted(self, user_id: str, *, day: str | None = None) -> bool:
        return self.used_today(user_id, day=day) >= self._limit

    def remaining_for_free_tier(self, user_id: str, *, day: str | None = None) -> int:
        return max(0, self._limit - self.used_today(user_id, day=day))
