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


def test_skips_keys_already_cached():
    calls = []
    cache = DictCache({"a": "old"})
    warmer = AnalysisCacheWarmer(cache, lambda key: calls.append(key) or "new")
    assert warmer.warm(["a", "b"]) == 1
    assert calls == ["b"]
    assert cache.data["a"] == "old"


def test_failed_key_is_skipped_and_others_still_warm():
    def analyzer(key):
        if key == "bad":
            raise RuntimeError("boom")
        return key

    cache = DictCache()
    assert AnalysisCacheWarmer(cache, analyzer).warm(["a", "bad", "b"]) == 2
    assert set(cache.data) == {"a", "b"}


def test_total_warmed_accumulates_across_calls():
    warmer = AnalysisCacheWarmer(DictCache(), lambda key: key)
    warmer.warm(["a"])
    warmer.warm(["b", "c"])
    assert warmer.total_warmed == 3
