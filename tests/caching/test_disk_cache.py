"""Tests for disk cache."""
from bird_mach.caching.disk_cache import DiskCache

class TestDiskCache:
    def test_set_get(self, tmp_path):
        c = DiskCache(tmp_path)
        c.set("k", {"data": 42})
        assert c.get("k") == {"data": 42}

    def test_miss(self, tmp_path):
        c = DiskCache(tmp_path)
        assert c.get("missing") is None

    def test_delete(self, tmp_path):
        c = DiskCache(tmp_path)
        c.set("k", {"x": 1})
        assert c.delete("k")
        assert c.get("k") is None

    def test_clear(self, tmp_path):
        c = DiskCache(tmp_path)
        c.set("a", {"v": 1})
        c.set("b", {"v": 2})
        n = c.clear()
        assert n == 2
        assert c.size == 0
