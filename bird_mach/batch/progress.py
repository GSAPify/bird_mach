"""Progress tracking for batch operations."""
from __future__ import annotations
from dataclasses import dataclass
import time

@dataclass
class BatchProgress:
    total: int
    completed: int = 0
    failed: int = 0
    started_at: float = 0.0

    @property
    def remaining(self) -> int:
        return self.total - self.completed - self.failed

    @property
    def percent(self) -> float:
        if self.total == 0:
            return 0.0
        return (self.completed + self.failed) / self.total * 100

    @property
    def elapsed_s(self) -> float:
        if self.started_at == 0:
            return 0.0
        return time.time() - self.started_at

    @property
    def eta_s(self) -> float:
        done = self.completed + self.failed
        if done == 0:
            return 0.0
        rate = self.elapsed_s / done
        return rate * self.remaining

    def tick_success(self) -> None:
        self.completed += 1

    def tick_failure(self) -> None:
        self.failed += 1

    def start(self) -> None:
        self.started_at = time.time()
