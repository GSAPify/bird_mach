"""Adaptive buffer management for streaming."""
from __future__ import annotations
from collections import deque

class AdaptiveBuffer:
    """Buffer that adjusts size based on network conditions."""
    def __init__(self, min_size: int = 4096, max_size: int = 65536):
        self._min = min_size
        self._max = max_size
        self._current_size = min_size
        self._data = deque()
        self._underruns = 0
        self._overflows = 0

    def push(self, chunk: bytes) -> bool:
        total = sum(len(c) for c in self._data) + len(chunk)
        if total > self._max:
            self._overflows += 1
            return False
        self._data.append(chunk)
        return True

    def pull(self, size: int) -> bytes:
        result = b""
        while self._data and len(result) < size:
            chunk = self._data.popleft()
            result += chunk
        if len(result) < size:
            self._underruns += 1
        return result[:size]

    def adapt(self, latency_ms: float) -> None:
        if latency_ms > 200:
            self._current_size = min(self._current_size * 2, self._max)
        elif latency_ms < 50 and self._current_size > self._min:
            self._current_size = max(self._current_size // 2, self._min)

    @property
    def stats(self) -> dict:
        return {"size": self._current_size, "underruns": self._underruns,
                "overflows": self._overflows, "buffered": sum(len(c) for c in self._data)}
