"""Object pool for audio frame reuse to reduce GC pressure."""
from __future__ import annotations
import numpy as np
from collections import deque

class FramePool:
    """Pool of pre-allocated numpy arrays for audio frames."""

    def __init__(self, frame_size: int = 2048, pool_size: int = 32):
        self._pool: deque[np.ndarray] = deque(
            (np.zeros(frame_size, dtype=np.float32) for _ in range(pool_size)),
            maxlen=pool_size,
        )
        self._frame_size = frame_size
        self._allocated = 0
        self._reused = 0

    def acquire(self) -> np.ndarray:
        if self._pool:
            self._reused += 1
            return self._pool.popleft()
        self._allocated += 1
        return np.zeros(self._frame_size, dtype=np.float32)

    def release(self, frame: np.ndarray) -> None:
        if frame.shape != (self._frame_size,):
            return
        frame[:] = 0
        if len(self._pool) < self._pool.maxlen:
            self._pool.append(frame)

    @property
    def stats(self) -> dict:
        return {"pool_size": len(self._pool), "allocated": self._allocated, "reused": self._reused}
