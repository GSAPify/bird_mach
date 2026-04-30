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
        if max_size < 1:
            raise ValueError("max_size must be at least 1")
        self._max = max_size
        self._ttl = ttl_s
        self._store: OrderedDict[str, CacheEntry] = OrderedDict()
        self._hits = 0
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
        self._hits += 1
        self._store.move_to_end(key)
        return entry.value

    def set(self, key: str, value: object, ttl_s: float | None = None) -> None:
        if key in self._store:
            self._store.pop(key)
        else:
            self._evict_expired()
            if len(self._store) >= self._max:
                self._store.popitem(last=False)
        self._store[key] = CacheEntry(
            value=value,
            expires_at=time.time() + (self._ttl if ttl_s is None else ttl_s),
        )

    def _evict_expired(self) -> None:
        now = time.time()
        for key in [k for k, e in self._store.items() if now > e.expires_at]:
            self._store.pop(key, None)

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
        return {"size": self.size, "hits": self._hits, "misses": self._misses}
