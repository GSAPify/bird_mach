"""Two-tier cache combining memory and disk layers."""
from __future__ import annotations
from pathlib import Path
from bird_mach.caching.memory_cache import MemoryCache
from bird_mach.caching.disk_cache import DiskCache

class TieredCache:
    def __init__(self, cache_dir: Path, mem_max: int = 500, mem_ttl: float = 120.0,
                 disk_ttl: float = 3600.0):
        self._l1 = MemoryCache(max_size=mem_max, ttl_s=mem_ttl)
        self._l2 = DiskCache(cache_dir, ttl_s=disk_ttl)

    def get(self, key: str):
        val = self._l1.get(key)
        if val is not None:
            return val
        val = self._l2.get(key)
        if val is not None:
            self._l1.set(key, val)
        return val

    def set(self, key: str, value, ttl_s: float | None = None) -> None:
        self._l1.set(key, value, ttl_s)
        if isinstance(value, dict):
            self._l2.set(key, value, ttl_s)

    def invalidate(self, key: str) -> None:
        self._l1.delete(key)
        self._l2.delete(key)

    def clear_all(self) -> dict:
        return {"memory": self._l1.clear(), "disk": self._l2.clear()}

    @property
    def stats(self) -> dict:
        return {"l1": self._l1.stats, "l2_size": self._l2.size}
