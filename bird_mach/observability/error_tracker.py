"""Centralized error tracking and aggregation."""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class TrackedError:
    type: str
    message: str
    count: int = 1
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)

class ErrorTracker:
    def __init__(self, max_unique: int = 500):
        self._errors: dict[str, TrackedError] = {}
        self._max = max_unique
        self._total = 0

    def track(self, error: Exception) -> TrackedError:
        self._total += 1
        key = f"{type(error).__name__}:{str(error)[:100]}"
        if key in self._errors:
            self._errors[key].count += 1
            self._errors[key].last_seen = datetime.now()
        else:
            if len(self._errors) < self._max:
                self._errors[key] = TrackedError(type=type(error).__name__, message=str(error))
        return self._errors.get(key, TrackedError(type(error).__name__, str(error)))

    def top_errors(self, n: int = 10) -> list[TrackedError]:
        return sorted(self._errors.values(), key=lambda e: -e.count)[:n]

    @property
    def total_errors(self) -> int:
        return self._total

    @property
    def unique_errors(self) -> int:
        return len(self._errors)
