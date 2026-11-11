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


def test_promotion_uses_remaining_disk_lifetime(tmp_path, monkeypatch):
    import bird_mach.caching.disk_cache as disk_mod
    import bird_mach.caching.memory_cache as mem_mod
    clock = [1000.0]
    monkeypatch.setattr(disk_mod.time, "time", lambda: clock[0])
    monkeypatch.setattr(mem_mod.time, "time", lambda: clock[0])
    if hasattr(mem_mod.time, "monotonic"):
        monkeypatch.setattr(mem_mod.time, "monotonic", lambda: clock[0])
    tc = TieredCache(tmp_path, mem_ttl=120.0, disk_ttl=100.0)
    tc._l2.set("k", {"v": 1})
    clock[0] += 95  # 5 s of disk lifetime left
    assert tc.get("k") == {"v": 1}
    clock[0] += 10  # past the disk entry's expiry
    assert tc._l1.get("k") is None
