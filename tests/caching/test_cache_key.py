"""Tests for cache key generation."""
from bird_mach.caching.cache_key import make_key, content_hash, params_hash, analysis_cache_key

class TestCacheKey:
    def test_make_key(self):
        assert make_key("a", "b", "c") == "a:b:c"

    def test_content_hash(self):
        h = content_hash(b"hello world")
        assert len(h) == 16

    def test_params_hash_deterministic(self):
        h1 = params_hash(sr=22050, hop=512)
        h2 = params_hash(hop=512, sr=22050)
        assert h1 == h2

    def test_analysis_key(self):
        k = analysis_cache_key("abc123", 22050, 512, 128)
        assert "analysis" in k
        assert "abc123" in k
