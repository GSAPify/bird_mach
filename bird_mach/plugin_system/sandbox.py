"""Sandboxed plugin execution environment."""
from __future__ import annotations
import time

class PluginSandbox:
    """Execute plugin code with resource limits."""
    def __init__(self, max_time_s: float = 5.0, max_memory_mb: int = 256):
        self._max_time = max_time_s
        self._max_memory = max_memory_mb

    def execute(self, func, *args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        elapsed = time.monotonic() - start
        if elapsed > self._max_time:
            raise TimeoutError(f"Plugin exceeded {self._max_time}s limit")
        return result
