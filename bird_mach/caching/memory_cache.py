"""In-memory LRU cache with TTL support."""
from __future__ import annotations
import time
from collections import OrderedDict
from dataclasses import dataclass

@dataclass
class CacheEntry:
    value: object
    expires_at: float
    hits: int = 0

class MemoryCache:
    def __init__(self, max_size: int = 1000, ttl_s: float = 300.0):
        self._max = max_size
        self._ttl = ttl_s
        self._store: OrderedDict[str, CacheEntry] = OrderedDict()
        self._misses = 0

    def get(self, key: str) -> object | None:
        entry = self._store.get(key)
        if entry is None:
            self._misses += 1
            return None
        if time.time() > entry.expires_at:
            self._store.pop(key, None)
            self._misses += 1
            return None
        entry.hits += 1
        self._store.move_to_end(key)
        return entry.value

    def set(self, key: str, value: object, ttl_s: float | None = None) -> None:
        if key in self._store:
            self._store.pop(key)
        elif len(self._store) >= self._max:
            self._store.popitem(last=False)
        self._store[key] = CacheEntry(
            value=value, expires_at=time.time() + (ttl_s or self._ttl),
        )

    def delete(self, key: str) -> bool:
        return self._store.pop(key, None) is not None

    def clear(self) -> int:
        n = len(self._store)
        self._store.clear()
        return n

    @property
    def size(self) -> int:
        return len(self._store)

    @property
    def stats(self) -> dict:
        total_hits = sum(e.hits for e in self._store.values())
        return {"size": self.size, "hits": total_hits, "misses": self._misses}
