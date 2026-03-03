"""Tests for bird_mach.cache."""

from bird_mach.cache import AnalysisCache


class TestAnalysisCache:
    def test_put_and_get(self):
        cache = AnalysisCache(max_size=5)
        cache.put("abc", {"result": 42})
        assert cache.get("abc") == {"result": 42}

    def test_miss_returns_none(self):
        cache = AnalysisCache()
        assert cache.get("nonexistent") is None

    def test_eviction(self):
        cache = AnalysisCache(max_size=2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.get("c") == 3

    def test_clear(self):
        cache = AnalysisCache()
        cache.put("x", 1)
        cache.clear()
        assert cache.size == 0

    def test_content_hash(self):
        h = AnalysisCache.content_hash(b"hello")
        assert isinstance(h, str)
        assert len(h) == 16
