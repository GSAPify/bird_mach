"""Tests for activity feed."""
from bird_mach.dashboard.activity_feed import ActivityFeed

class TestActivityFeed:
    def test_log_activity(self):
        feed = ActivityFeed()
        a = feed.log("u1", "upload", "audio", "a1")
        assert a.action == "upload"
        assert feed.total_activities == 1

    def test_get_recent(self):
        feed = ActivityFeed()
        for i in range(5):
            feed.log("u1", "analyze", "audio", f"a{i}")
        recent = feed.get_recent(3)
        assert len(recent) == 3

    def test_get_for_user(self):
        feed = ActivityFeed()
        feed.log("u1", "upload", "audio", "a1")
        feed.log("u2", "upload", "audio", "a2")
        assert len(feed.get_for_user("u1")) == 1

    def test_max_items(self):
        feed = ActivityFeed(max_items=5)
        for i in range(10):
            feed.log("u1", "x", "y", str(i))
        assert feed.total_activities == 5
