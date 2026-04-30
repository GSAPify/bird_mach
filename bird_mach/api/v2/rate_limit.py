"""API v2 rate limiting middleware."""
from __future__ import annotations
import time
from dataclasses import dataclass

@dataclass
class RateLimitInfo:
    allowed: bool
    limit: int
    remaining: int
    reset_at: float
    retry_after_s: float = 0.0

class SlidingWindowLimiter:
    """Sliding window rate limiter for API endpoints."""
    def __init__(self, window_s: float = 60.0, max_requests: int = 100):
        if window_s <= 0:
            raise ValueError("window_s must be positive")
        if max_requests < 1:
            raise ValueError("max_requests must be at least 1")
        self._window = window_s
        self._max = max_requests
        self._requests: dict[str, list[float]] = {}

    def check(self, key: str) -> RateLimitInfo:
        now = time.time()
        cutoff = now - self._window
        timestamps = [t for t in self._requests.get(key, []) if t > cutoff]
        self._requests[key] = timestamps
        remaining = self._max - len(timestamps)
        if remaining > 0:
            timestamps.append(now)
            return RateLimitInfo(
                allowed=True, limit=self._max,
                remaining=remaining - 1, reset_at=now + self._window,
            )
        oldest = min(timestamps) if timestamps else now
        retry = oldest + self._window - now
        return RateLimitInfo(
            allowed=False, limit=self._max, remaining=0,
            reset_at=oldest + self._window, retry_after_s=retry,
        )
