import pytest
"""Tests for presence tracker."""
from bird_mach.collaboration.presence import PresenceTracker
class TestPresence:
    def test_update(self):
        pt = PresenceTracker()
        pt.update("u1", status="online")
        assert pt.online_count == 1
    def test_remove(self):
        pt = PresenceTracker()
        pt.update("u1")
        pt.remove("u1")
        assert pt.online_count == 0


def test_negative_cursor_time_rejected():
    from bird_mach.collaboration.presence import PresenceTracker
    tracker = PresenceTracker()
    with pytest.raises(ValueError):
        tracker.update("u1", cursor_time_s=-2.0)
    assert tracker.online_count == 0
