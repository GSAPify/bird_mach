"""Monitor audio processing latency."""
from __future__ import annotations
import math
import time
from collections import deque

class LatencyMonitor:
    """Track processing latency across frames."""

    def __init__(self, window: int = 100):
        self._latencies = deque(maxlen=window)

    def record(self, start_ns: int) -> float:
        elapsed_ms = (time.time_ns() - start_ns) / 1e6
        self._latencies.append(elapsed_ms)
        return elapsed_ms

    @property
    def avg_ms(self) -> float:
        return sum(self._latencies) / max(len(self._latencies), 1)

    @property
    def max_ms(self) -> float:
        return max(self._latencies) if self._latencies else 0.0

    @property
    def p99_ms(self) -> float:
        if len(self._latencies) < 2:
            return self.max_ms
        sorted_lat = sorted(self._latencies)
        idx = math.ceil(0.99 * len(sorted_lat)) - 1
        return sorted_lat[max(0, min(idx, len(sorted_lat) - 1))]

    @property
    def is_healthy(self) -> bool:
        return self.avg_ms < 50.0
