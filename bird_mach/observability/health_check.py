"""Health check endpoints and system status."""
from __future__ import annotations
import time
import platform
from collections.abc import Callable
from dataclasses import dataclass

@dataclass
class HealthStatus:
    status: str
    version: str
    uptime_s: float
    python_version: str
    checks: dict[str, bool]

    @property
    def is_healthy(self) -> bool:
        return self.status == "healthy" and all(self.checks.values())

class HealthChecker:
    def __init__(self, version: str = "0.5.0"):
        self._version = version
        self._start_time = time.time()
        self._checks: dict[str, Callable[[], bool]] = {}

    def register_check(self, name: str, check_fn: Callable[[], bool]) -> None:
        self._checks[name] = check_fn

    def run(self) -> HealthStatus:
        results = {}
        for name, fn in self._checks.items():
            try:
                results[name] = fn()
            except Exception:
                results[name] = False
        status = "healthy" if all(results.values()) else "degraded"
        if not results:
            status = "healthy"
        return HealthStatus(
            status=status, version=self._version,
            uptime_s=time.time() - self._start_time,
            python_version=platform.python_version(),
            checks=results,
        )
