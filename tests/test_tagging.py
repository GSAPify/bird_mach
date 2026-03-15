"""Tests for tagging."""
from bird_mach.tagging import TagManager
class TestTagManager:
    def test_tag(self):
        tm = TagManager()
        tm.tag("a1", "jazz")
        assert "jazz" in tm.get_tags("a1")
    def test_find_by_tag(self):
        tm = TagManager()
        tm.tag("a1", "rock")
        tm.tag("a2", "rock")
        assert len(tm.find_by_tag("rock")) == 2
    def test_untag(self):
        tm = TagManager()
        tm.tag("a1", "pop")
        tm.untag("a1", "pop")
        assert "pop" not in tm.get_tags("a1")
    def test_popular(self):
        tm = TagManager()
        for i in range(5): tm.tag(f"a{i}", "common")
        tm.tag("a0", "rare")
        top = tm.popular_tags()
        assert top[0][0] == "common"
