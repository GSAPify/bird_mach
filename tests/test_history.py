"""Tests for history."""
from bird_mach.history import HistoryTracker
class TestHistory:
    def test_record(self):
        ht = HistoryTracker()
        ht.record("a1", "u1", "analyze", stride=2)
        assert ht.total == 1
    def test_recent(self):
        ht = HistoryTracker()
        ht.record("a1", "u1", "analyze")
        ht.record("a2", "u2", "analyze")
        assert len(ht.get_recent("u1")) == 1
    def test_for_audio(self):
        ht = HistoryTracker()
        ht.record("a1", "u1", "upload")
        ht.record("a1", "u2", "analyze")
        assert len(ht.get_for_audio("a1")) == 2
