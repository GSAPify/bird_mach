"""Tests for the auth audit log."""

from __future__ import annotations

import pytest

from bird_mach.auth.audit import (
    AuthEvent,
    AuthEventType,
    InMemoryAuditLog,
    SqliteAuditLog,
)
from bird_mach.db import Database


@pytest.fixture(params=["memory", "sqlite"])
def log(request):
    if request.param == "memory":
        return InMemoryAuditLog()
    return SqliteAuditLog(Database(":memory:"))


class TestAuditLog:
    def test_record_and_retrieve(self, log):
        log.record(AuthEvent(AuthEventType.LOGIN_SUCCESS, user_id="u1", ip="1.1.1.1"))
        events = log.recent_for_user("u1")
        assert len(events) == 1
        assert events[0].event_type is AuthEventType.LOGIN_SUCCESS
        assert events[0].ip == "1.1.1.1"

    def test_failures_without_user_are_not_attributed(self, log):
        log.record(AuthEvent(AuthEventType.LOGIN_FAILURE, email="ghost@x.com"))
        assert log.recent_for_user("u1") == []

    def test_recent_is_newest_first_and_limited(self, log):
        for _ in range(5):
            log.record(AuthEvent(AuthEventType.LOGIN_SUCCESS, user_id="u1"))
        events = log.recent_for_user("u1", limit=3)
        assert len(events) == 3
        assert events[0].created_at >= events[-1].created_at

    def test_events_are_per_user(self, log):
        log.record(AuthEvent(AuthEventType.REGISTERED, user_id="u1"))
        log.record(AuthEvent(AuthEventType.REGISTERED, user_id="u2"))
        assert len(log.recent_for_user("u1")) == 1


def test_public_dict_shape():
    e = AuthEvent(AuthEventType.PASSWORD_CHANGED, user_id="u1", email="a@b.com")
    d = e.public_dict()
    assert d["event_type"] == "password_changed"
    assert set(d) == {"id", "event_type", "user_id", "email", "ip", "created_at"}
