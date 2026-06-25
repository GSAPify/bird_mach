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

    def test_maxlen_eviction(self):
        """Entries beyond max_entries must be silently dropped (FIFO eviction)."""
        ht = HistoryTracker(max_entries=3)
        for i in range(5):
            ht.record(f"a{i}", "u1", "analyze")
        # Only the last 3 must be retained
        assert ht.total == 3
        ids = {e.audio_id for e in ht.get_recent("u1", n=10)}
        assert "a0" not in ids
        assert "a4" in ids

    def test_get_recent_order(self):
        """get_recent must return most-recent entries first."""
        ht = HistoryTracker()
        ht.record("a1", "u1", "upload")
        ht.record("a2", "u1", "analyze")
        entries = ht.get_recent("u1")
        assert entries[0].audio_id == "a2"
