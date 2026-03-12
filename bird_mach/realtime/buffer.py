"""Ring buffer for low-latency audio frame management."""
from __future__ import annotations
import numpy as np

class RingBuffer:
    """Fixed-size circular buffer for audio samples."""

    def __init__(self, capacity: int, dtype=np.float32) -> None:
        self._buf = np.zeros(capacity, dtype=dtype)
        self._capacity = capacity
        self._write_pos = 0
        self._count = 0

    def write(self, data: np.ndarray) -> None:
        n = len(data)
        if n >= self._capacity:
            self._buf[:] = data[-self._capacity:]
            self._write_pos = 0
            self._count = self._capacity
            return
        end = self._write_pos + n
        if end <= self._capacity:
            self._buf[self._write_pos:end] = data
        else:
            first = self._capacity - self._write_pos
            self._buf[self._write_pos:] = data[:first]
            self._buf[:n - first] = data[first:]
        self._write_pos = end % self._capacity
        self._count = min(self._count + n, self._capacity)

    def read(self, n: int | None = None) -> np.ndarray:
        if n is None:
            n = self._count
        n = min(n, self._count)
        start = (self._write_pos - n) % self._capacity
        if start + n <= self._capacity:
            return self._buf[start:start + n].copy()
        first = self._capacity - start
        return np.concatenate([self._buf[start:], self._buf[:n - first]])

    @property
    def count(self) -> int:
        return self._count

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def is_full(self) -> bool:
        return self._count >= self._capacity

    def clear(self) -> None:
        self._buf[:] = 0
        self._write_pos = 0
        self._count = 0
