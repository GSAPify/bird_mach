"""Tests for tiered cache."""
from bird_mach.caching.tiered_cache import TieredCache

class TestTieredCache:
    def test_set_get(self, tmp_path):
        tc = TieredCache(tmp_path)
        tc.set("k", {"val": 1})
        assert tc.get("k") == {"val": 1}

    def test_l2_promotion(self, tmp_path):
        tc = TieredCache(tmp_path, mem_max=1)
        tc.set("a", {"v": 1})
        tc.set("b", {"v": 2})
        val = tc.get("a")
        assert val == {"v": 1}

    def test_invalidate(self, tmp_path):
        tc = TieredCache(tmp_path)
        tc.set("k", {"v": 1})
        tc.invalidate("k")
        assert tc.get("k") is None
