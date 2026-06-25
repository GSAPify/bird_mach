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

    def test_get_tags_returns_copy(self):
        """Mutating the returned set must not corrupt internal state."""
        tm = TagManager()
        tm.tag("a1", "jazz")
        tags = tm.get_tags("a1")
        tags.add("poison")
        assert "poison" not in tm.get_tags("a1")

    def test_find_by_tag_returns_copy(self):
        """Mutating the returned set must not corrupt the reverse index."""
        tm = TagManager()
        tm.tag("a1", "rock")
        resources = tm.find_by_tag("rock")
        resources.add("phantom")
        assert "phantom" not in tm.find_by_tag("rock")
