"""Tests for subscription repositories (both backends, same cases)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from bird_mach.billing.models import Subscription, SubscriptionStatus
from bird_mach.billing.store import (
    InMemorySubscriptionRepository,
    SqliteSubscriptionRepository,
)
from bird_mach.db import Database


@pytest.fixture(params=["memory", "sqlite"])
def repo(request):
    if request.param == "memory":
        return InMemorySubscriptionRepository()
    return SqliteSubscriptionRepository(Database(":memory:"))


def _sub(sub_id="s1", user="u1", status=SubscriptionStatus.ACTIVE, stripe_id="sub_1", created=None):
    return Subscription(
        id=sub_id,
        user_id=user,
        plan_id="pro",
        status=status,
        stripe_subscription_id=stripe_id,
        created_at=created or datetime.now(timezone.utc),
    )


class TestSubscriptionRepository:
    def test_upsert_and_get(self, repo):
        repo.upsert(_sub())
        assert repo.get("s1").status is SubscriptionStatus.ACTIVE

    def test_upsert_updates_existing(self, repo):
        repo.upsert(_sub())
        sub = repo.get("s1")
        sub.status = SubscriptionStatus.CANCELED
        repo.upsert(sub)
        assert repo.get("s1").status is SubscriptionStatus.CANCELED

    def test_get_by_user(self, repo):
        repo.upsert(_sub())
        assert repo.get_by_user("u1").id == "s1"
        assert repo.get_by_user("missing") is None

    def test_get_by_user_returns_latest(self, repo):
        base = datetime(2026, 1, 1, tzinfo=timezone.utc)
        repo.upsert(_sub(sub_id="old", stripe_id="sub_old", created=base))
        repo.upsert(
            _sub(sub_id="new", stripe_id="sub_new", created=base + timedelta(days=30))
        )
        assert repo.get_by_user("u1").id == "new"

    def test_get_by_stripe_id(self, repo):
        repo.upsert(_sub(stripe_id="sub_xyz"))
        assert repo.get_by_stripe_id("sub_xyz").id == "s1"
        assert repo.get_by_stripe_id("nope") is None
