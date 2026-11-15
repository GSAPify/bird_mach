"""Tests for cache warming."""
from bird_mach.caching.warming import AnalysisCacheWarmer


class DictCache:
    def __init__(self, data=None):
        self.data = dict(data or {})

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value


def test_warms_cold_keys_and_returns_count():
    cache = DictCache()
    warmer = AnalysisCacheWarmer(cache, lambda key: f"result:{key}")
    assert warmer.warm(["a", "b"]) == 2
    assert cache.data == {"a": "result:a", "b": "result:b"}
