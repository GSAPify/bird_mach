"""Tests for audit log."""
from bird_mach.observability.audit_log import AuditLog

class TestAuditLog:
    def test_record(self):
        log = AuditLog()
        entry = log.record("u1", "login", "session", ip="10.0.0.1")
        assert entry.action == "login"
        assert log.total_entries == 1

    def test_query_by_user(self):
        log = AuditLog()
        log.record("u1", "upload", "audio")
        log.record("u2", "delete", "audio")
        assert len(log.query(user_id="u1")) == 1

    def test_query_by_action(self):
        log = AuditLog()
        log.record("u1", "login", "session")
        log.record("u1", "upload", "audio")
        assert len(log.query(action="login")) == 1

    def test_immutable(self):
        log = AuditLog()
        entry = log.record("u1", "test", "res")
        try:
            entry.action = "changed"
            assert False
        except AttributeError:
            pass
