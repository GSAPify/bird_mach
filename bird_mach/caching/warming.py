"""Cache warming strategies."""
from __future__ import annotations
import logging
from typing import Protocol

logger = logging.getLogger(__name__)

class CacheWarmer(Protocol):
    def warm(self, keys: list[str]) -> int: ...

class AnalysisCacheWarmer:
    """Pre-populate cache with frequently accessed analyses."""
    def __init__(self, cache, analyzer):
        self._cache = cache
        self._analyzer = analyzer
        self._warmed = 0

    def warm(self, keys: list[str]) -> int:
        for key in keys:
            if self._cache.get(key) is None:
                try:
                    result = self._analyzer(key)
                    self._cache.set(key, result)
                    self._warmed += 1
                except Exception as e:
                    logger.warning("Failed to warm key %s: %s", key, e)
        return self._warmed

    @property
    def total_warmed(self) -> int:
        return self._warmed
