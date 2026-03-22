"""Retry policy for failed webhook deliveries."""
from __future__ import annotations
from dataclasses import dataclass
import time

@dataclass
class RetryPolicy:
    max_retries: int = 5
    base_delay_s: float = 1.0
    max_delay_s: float = 300.0
    backoff_factor: float = 2.0

    def get_delay(self, attempt: int) -> float:
        delay = self.base_delay_s * (self.backoff_factor ** attempt)
        return min(delay, self.max_delay_s)

    def should_retry(self, attempt: int) -> bool:
        return attempt < self.max_retries

class RetryQueue:
    def __init__(self, policy: RetryPolicy | None = None):
        self._policy = policy or RetryPolicy()
        self._items: list[dict] = []

    def enqueue(self, event_data: dict, attempt: int = 0) -> None:
        if self._policy.should_retry(attempt):
            delay = self._policy.get_delay(attempt)
            self._items.append({"data": event_data, "attempt": attempt + 1,
                               "retry_at": time.time() + delay})

    def get_due(self) -> list[dict]:
        now = time.time()
        due = [i for i in self._items if i["retry_at"] <= now]
        self._items = [i for i in self._items if i["retry_at"] > now]
        return due

    @property
    def pending_count(self) -> int:
        return len(self._items)
