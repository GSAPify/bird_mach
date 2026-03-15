"""Tests for usage tracker."""
from bird_mach.dashboard.usage_tracker import UsageTracker

class TestUsageTracker:
    def test_record_and_get(self):
        tracker = UsageTracker()
        tracker.record("user1")
        assert tracker.get_usage("user1") == 1

    def test_quota_check(self):
        tracker = UsageTracker(default_quota=5)
        for _ in range(4):
            tracker.record("user1")
        ok, used, quota = tracker.check_quota("user1")
        assert ok
        assert used == 4

    def test_quota_exceeded(self):
        tracker = UsageTracker(default_quota=2)
        tracker.record("user1")
        tracker.record("user1")
        ok, _, _ = tracker.check_quota("user1")
        assert not ok

    def test_top_users(self):
        tracker = UsageTracker()
        for _ in range(10):
            tracker.record("heavy-user")
        tracker.record("light-user")
        top = tracker.get_top_users(2)
        assert top[0][0] == "heavy-user"
