"""Cache invalidation strategy variant 2."""
from __future__ import annotations

class InvalidationStrategy2:
    """Strategy 2: event-based invalidation."""
    def __init__(self):
        self._invalidated = 0
    def invalidate(self, key: str) -> bool:
        self._invalidated += 1
        return True
    @property
    def count(self) -> int:
        return self._invalidated
