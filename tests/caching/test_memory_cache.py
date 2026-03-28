"""Tests for memory cache."""
import time
from bird_mach.caching.memory_cache import MemoryCache

class TestMemoryCache:
    def test_set_get(self):
        c = MemoryCache()
        c.set("k", "v")
        assert c.get("k") == "v"

    def test_miss(self):
        c = MemoryCache()
        assert c.get("nope") is None

    def test_ttl_expiry(self):
        c = MemoryCache(ttl_s=0.01)
        c.set("k", "v")
        time.sleep(0.02)
        assert c.get("k") is None

    def test_lru_eviction(self):
        c = MemoryCache(max_size=2)
        c.set("a", 1)
        c.set("b", 2)
        c.set("c", 3)
        assert c.get("a") is None
        assert c.get("c") == 3

    def test_delete(self):
        c = MemoryCache()
        c.set("k", "v")
        assert c.delete("k")
        assert c.get("k") is None

    def test_stats(self):
        c = MemoryCache()
        c.set("k", "v")
        c.get("k")
        s = c.stats
        assert s["hits"] == 1
