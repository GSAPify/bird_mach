"""Cache invalidation strategy variant 3."""
from __future__ import annotations

class InvalidationStrategy3:
    """Strategy 3: hybrid invalidation."""
    def __init__(self):
        self._invalidated = 0
    def invalidate(self, key: str) -> bool:
        self._invalidated += 1
        return True
    @property
    def count(self) -> int:
        return self._invalidated
