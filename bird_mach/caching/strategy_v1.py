"""Cache invalidation strategy variant 1."""
from __future__ import annotations

class InvalidationStrategy1:
    """Strategy 1: time-based invalidation."""
    def __init__(self):
        self._invalidated = 0
    def invalidate(self, key: str) -> bool:
        self._invalidated += 1
        return True
    @property
    def count(self) -> int:
        return self._invalidated
