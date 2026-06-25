"""Tests for favorites."""
from bird_mach.favorites import FavoritesManager
class TestFavorites:
    def test_add_and_check(self):
        fm = FavoritesManager()
        fm.add("u1", "a1")
        assert fm.is_favorite("u1", "a1")
    def test_remove(self):
        fm = FavoritesManager()
        fm.add("u1", "a1")
        fm.remove("u1", "a1")
        assert not fm.is_favorite("u1", "a1")
    def test_count(self):
        fm = FavoritesManager()
        fm.add("u1", "a1")
        fm.add("u1", "a2")
        assert fm.count("u1") == 2

    def test_remove_nonexistent_user_no_side_effect(self):
        """remove() on unknown user must not create a spurious dict entry."""
        fm = FavoritesManager()
        fm.remove("ghost", "a1")
        # The defaultdict must not have auto-created an entry for "ghost"
        assert fm.count("ghost") == 0
        assert not fm.is_favorite("ghost", "a1")

    def test_get_returns_newest_first(self):
        """get() must return audio IDs ordered newest-added first."""
        import time
        fm = FavoritesManager()
        fm.add("u1", "old")
        time.sleep(0.01)
        fm.add("u1", "new")
        assert fm.get("u1")[0] == "new"
