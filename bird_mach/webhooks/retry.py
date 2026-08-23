"""Retry policy for failed webhook deliveries."""
from __future__ import annotations
import logging
import time
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class RetryPolicy:
    max_retries: int = 5
    base_delay_s: float = 1.0
    max_delay_s: float = 300.0
    backoff_factor: float = 2.0

    def __post_init__(self) -> None:
        if self.max_retries < 0:
            raise ValueError("max_retries must not be negative")
        if self.base_delay_s < 0 or self.max_delay_s < 0:
            raise ValueError("delays must not be negative")
        if self.backoff_factor < 1:
            raise ValueError("backoff_factor must be at least 1")

    def get_delay(self, attempt: int) -> float:
        try:
            delay = self.base_delay_s * (self.backoff_factor ** attempt)
        except OverflowError:
            # A large attempt count overflows before min() can cap it.
            return self.max_delay_s
        return min(delay, self.max_delay_s)

    def should_retry(self, attempt: int) -> bool:
        return attempt < self.max_retries

class RetryQueue:
    def __init__(self, policy: RetryPolicy | None = None, max_pending: int = 10000):
        if max_pending < 1:
            raise ValueError("max_pending must be at least 1")
        self._policy = policy or RetryPolicy()
        self._max_pending = max_pending
        self._items: list[dict] = []

    def enqueue(self, event_data: dict, attempt: int = 0) -> bool:
        """Schedule a retry. False means the delivery was given up on."""
        if not self._policy.should_retry(attempt):
            logger.warning("Retries exhausted after %d attempts, dropping event", attempt)
            return False
        if len(self._items) >= self._max_pending:
            logger.warning("Retry queue full (%d), dropping event", self._max_pending)
            return False
        delay = self._policy.get_delay(attempt)
        self._items.append({"data": event_data, "attempt": attempt + 1,
                           "retry_at": time.time() + delay})
        return True

    def get_due(self) -> list[dict]:
        now = time.time()
        due = [i for i in self._items if i["retry_at"] <= now]
        self._items = [i for i in self._items if i["retry_at"] > now]
        return due

    @property
    def pending_count(self) -> int:
        return len(self._items)
