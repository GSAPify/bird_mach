"""SDK retry logic with jitter."""
from __future__ import annotations
import random
import time
from collections.abc import Callable
from typing import Any

class RetryConfig:
    def __init__(self, max_retries: int = 3, base_delay: float = 0.5, jitter: bool = True):
        if max_retries < 0:
            raise ValueError("max_retries must not be negative")
        if base_delay < 0:
            raise ValueError("base_delay must not be negative")
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.jitter = jitter

    def delay_for(self, attempt: int) -> float:
        delay = self.base_delay * (2 ** attempt)
        if self.jitter:
            delay *= (0.5 + random.random())
        return min(delay, 30.0)

def with_retry(fn: Callable[[], Any], config: RetryConfig | None = None) -> Any:
    cfg = config or RetryConfig()
    last_err = None
    for attempt in range(cfg.max_retries + 1):
        try:
            return fn()
        except Exception as e:
            last_err = e
            if attempt < cfg.max_retries:
                time.sleep(cfg.delay_for(attempt))
    if last_err is None:
        raise RuntimeError("retry loop exited without a result or error")
    raise last_err
