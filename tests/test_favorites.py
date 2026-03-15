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
