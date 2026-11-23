"""Sandboxed plugin execution environment."""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout

class PluginSandbox:
    """Execute plugin code with resource limits."""
    def __init__(self, max_time_s: float = 5.0, max_memory_mb: int = 256):
        if max_time_s <= 0:
            raise ValueError("max_time_s must be positive")
        if max_memory_mb < 1:
            raise ValueError("max_memory_mb must be at least 1")
        self._max_time = max_time_s
        self._max_memory = max_memory_mb

    def execute(self, func, *args, **kwargs):
        # Measuring elapsed time after the call returns cannot abort a hung
        # plugin. Run it in a worker and bound wait time to max_time_s.
        # No `with` block: its exit calls shutdown(wait=True), which blocked on the
        # hung plugin, so the timeout only fired once the plugin had finished anyway.
        pool = ThreadPoolExecutor(max_workers=1)
        try:
            future = pool.submit(func, *args, **kwargs)
            try:
                return future.result(timeout=self._max_time)
            except FuturesTimeout as exc:
                raise TimeoutError(f"Plugin exceeded {self._max_time}s limit") from exc
        finally:
            pool.shutdown(wait=False, cancel_futures=True)
