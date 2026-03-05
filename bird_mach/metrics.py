"""Application metrics and counters."""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class AppMetrics:
    """Simple in-memory metrics for monitoring."""

    requests_total: int = 0
    analyses_total: int = 0
    errors_total: int = 0
    total_audio_seconds_processed: float = 0.0
    _start_time: float = field(default_factory=time.time)

    @property
    def uptime_s(self) -> float:
        return time.time() - self._start_time

    def record_request(self) -> None:
        self.requests_total += 1

    def record_analysis(self, duration_s: float) -> None:
        self.analyses_total += 1
        self.total_audio_seconds_processed += duration_s

    def record_error(self) -> None:
        self.errors_total += 1

    def to_dict(self) -> dict[str, float | int]:
        return {
            "requests_total": self.requests_total,
            "analyses_total": self.analyses_total,
            "errors_total": self.errors_total,
            "audio_seconds_processed": round(self.total_audio_seconds_processed, 1),
            "uptime_s": round(self.uptime_s, 1),
        }
