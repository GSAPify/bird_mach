"""Token bucket rate limiter for API protection."""
from __future__ import annotations
import time
from dataclasses import dataclass

@dataclass
class RateLimitResult:
    allowed: bool
    remaining: int
    reset_at: float

class TokenBucketLimiter:
    def __init__(self, capacity: int = 100, refill_rate: float = 10.0):
        self._capacity = capacity
        self._refill_rate = refill_rate
        self._buckets: dict[str, tuple[float, float]] = {}

    def check(self, key: str) -> RateLimitResult:
        now = time.time()
        tokens, last_refill = self._buckets.get(key, (float(self._capacity), now))
        elapsed = now - last_refill
        tokens = min(self._capacity, tokens + elapsed * self._refill_rate)
        if tokens >= 1:
            tokens -= 1
            self._buckets[key] = (tokens, now)
            return RateLimitResult(allowed=True, remaining=int(tokens), reset_at=now + (1/self._refill_rate))
        self._buckets[key] = (tokens, now)
        return RateLimitResult(allowed=False, remaining=0, reset_at=now + (1/self._refill_rate))
