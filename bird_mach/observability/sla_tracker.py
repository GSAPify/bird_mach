"""SLA tracking and uptime monitoring."""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass

@dataclass
class SLAReport:
    uptime_percent: float
    total_checks: int
    failures: int
    avg_response_ms: float
    p50_response_ms: float
    p95_response_ms: float
    p99_response_ms: float

class SLATracker:
    def __init__(self, window_size: int = 1000):
        self._checks: deque[tuple[bool, float]] = deque(maxlen=window_size)

    def record_check(self, success: bool, response_ms: float) -> None:
        self._checks.append((success, response_ms))

    def report(self) -> SLAReport:
        if not self._checks:
            return SLAReport(100.0, 0, 0, 0.0, 0.0, 0.0, 0.0)
        successes = sum(1 for s, _ in self._checks if s)
        failures = len(self._checks) - successes
        times = [t for _, t in self._checks]
        sorted_times = sorted(times)
        return SLAReport(
            uptime_percent=successes / len(self._checks) * 100,
            total_checks=len(self._checks),
            failures=failures,
            avg_response_ms=sum(times) / len(times),
            p50_response_ms=self._percentile(sorted_times, 0.50),
            p95_response_ms=self._percentile(sorted_times, 0.95),
            p99_response_ms=self._percentile(sorted_times, 0.99),
        )

    @staticmethod
    def _percentile(sorted_times: list[float], q: float) -> float:
        idx = min(int(len(sorted_times) * q), len(sorted_times) - 1)
        return sorted_times[idx]
