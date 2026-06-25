"""Tests for usage metering and free-tier quota logic."""

from __future__ import annotations

import pytest

from bird_mach.db import Database
from bird_mach.usage import (
    InMemoryUsageRepository,
    SqliteUsageRepository,
    UsageService,
)


@pytest.fixture(params=["memory", "sqlite"])
def repo(request):
    if request.param == "memory":
        return InMemoryUsageRepository()
    return SqliteUsageRepository(Database(":memory:"))


class TestUsageRepository:
    def test_increment_accumulates(self, repo):
        assert repo.increment("u1", "2026-06-25") == 1
        assert repo.increment("u1", "2026-06-25") == 2
        assert repo.count("u1", "2026-06-25") == 2

    def test_counts_are_per_user_and_day(self, repo):
        repo.increment("u1", "2026-06-25")
        assert repo.count("u2", "2026-06-25") == 0
        assert repo.count("u1", "2026-06-26") == 0


class TestUsageService:
    def test_free_tier_exhaustion(self):
        svc = UsageService(InMemoryUsageRepository(), free_daily_limit=3)
        day = "2026-06-25"
        for _ in range(3):
            assert not svc.free_tier_exhausted("u1", day=day)
            svc.record("u1", day=day)
        assert svc.free_tier_exhausted("u1", day=day)
        assert svc.remaining_for_free_tier("u1", day=day) == 0

    def test_remaining_counts_down(self):
        svc = UsageService(InMemoryUsageRepository(), free_daily_limit=5)
        day = "2026-06-25"
        svc.record("u1", day=day)
        svc.record("u1", day=day)
        assert svc.remaining_for_free_tier("u1", day=day) == 3
        assert svc.used_today("u1", day=day) == 2

    def test_sqlite_persists_across_handles(self, tmp_path):
        db = Database(tmp_path / "usage.db")
        UsageService(SqliteUsageRepository(db)).record("u1", day="2026-06-25")
        db.close()
        reopened = UsageService(SqliteUsageRepository(Database(tmp_path / "usage.db")))
        assert reopened.used_today("u1", day="2026-06-25") == 1
