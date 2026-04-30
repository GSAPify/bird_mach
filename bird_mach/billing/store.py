"""Subscription persistence with in-memory and SQLite backends.

Subscriptions are looked up two ways: by ``user_id`` (the paywall check on a
request) and by ``stripe_subscription_id`` (incoming webhooks, which only know
the Stripe id). Both backends index for both access paths.
"""

from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from datetime import datetime

from bird_mach.billing.models import Subscription, SubscriptionStatus
from bird_mach.db import Database

_SCHEMA = """
CREATE TABLE IF NOT EXISTS subscriptions (
    id                     TEXT PRIMARY KEY,
    user_id                TEXT NOT NULL,
    plan_id                TEXT NOT NULL,
    status                 TEXT NOT NULL,
    stripe_subscription_id TEXT,
    current_period_end     TEXT,
    created_at             TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_subs_user ON subscriptions (user_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_subs_stripe
    ON subscriptions (stripe_subscription_id)
    WHERE stripe_subscription_id IS NOT NULL;
"""


class SubscriptionRepository(ABC):
    @abstractmethod
    def upsert(self, sub: Subscription) -> Subscription: ...

    @abstractmethod
    def get(self, sub_id: str) -> Subscription | None: ...

    @abstractmethod
    def get_by_user(self, user_id: str) -> Subscription | None: ...

    @abstractmethod
    def get_by_stripe_id(self, stripe_subscription_id: str) -> Subscription | None: ...


class InMemorySubscriptionRepository(SubscriptionRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, Subscription] = {}
        self._lock = threading.RLock()

    def upsert(self, sub: Subscription) -> Subscription:
        with self._lock:
            self._by_id[sub.id] = sub
            return sub

    def get(self, sub_id: str) -> Subscription | None:
        return self._by_id.get(sub_id)

    def get_by_user(self, user_id: str) -> Subscription | None:
        # Prefer an entitling subscription: a newer incomplete/canceled row
        # must not hide the active one and silently drop access.
        subs = [s for s in self._by_id.values() if s.user_id == user_id]
        active = [s for s in subs if s.is_active]
        return max(active or subs, key=lambda s: s.created_at, default=None)

    def get_by_stripe_id(self, stripe_subscription_id: str) -> Subscription | None:
        return next(
            (
                s
                for s in self._by_id.values()
                if s.stripe_subscription_id == stripe_subscription_id
            ),
            None,
        )


class SqliteSubscriptionRepository(SubscriptionRepository):
    def __init__(self, db: Database) -> None:
        self._db = db
        self._db.executescript(_SCHEMA)

    @staticmethod
    def _row_to_sub(row) -> Subscription:
        end = row["current_period_end"]
        return Subscription(
            id=row["id"],
            user_id=row["user_id"],
            plan_id=row["plan_id"],
            status=SubscriptionStatus(row["status"]),
            stripe_subscription_id=row["stripe_subscription_id"],
            current_period_end=datetime.fromisoformat(end) if end else None,
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def upsert(self, sub: Subscription) -> Subscription:
        self._db.execute(
            "INSERT INTO subscriptions (id, user_id, plan_id, status, "
            "stripe_subscription_id, current_period_end, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(id) DO UPDATE SET plan_id=excluded.plan_id, "
            "status=excluded.status, "
            "stripe_subscription_id=excluded.stripe_subscription_id, "
            "current_period_end=excluded.current_period_end",
            [
                sub.id,
                sub.user_id,
                sub.plan_id,
                sub.status.value,
                sub.stripe_subscription_id,
                sub.current_period_end.isoformat() if sub.current_period_end else None,
                sub.created_at.isoformat(),
            ],
        )
        return sub

    def get(self, sub_id: str) -> Subscription | None:
        row = self._db.query_one("SELECT * FROM subscriptions WHERE id = ?", [sub_id])
        return self._row_to_sub(row) if row else None

    def get_by_user(self, user_id: str) -> Subscription | None:
        row = self._db.query_one(
            "SELECT * FROM subscriptions WHERE user_id = ? "
            "ORDER BY created_at DESC LIMIT 1",
            [user_id],
        )
        return self._row_to_sub(row) if row else None

    def get_by_stripe_id(self, stripe_subscription_id: str) -> Subscription | None:
        row = self._db.query_one(
            "SELECT * FROM subscriptions WHERE stripe_subscription_id = ?",
            [stripe_subscription_id],
        )
        return self._row_to_sub(row) if row else None
