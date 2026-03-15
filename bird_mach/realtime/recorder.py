"""In-memory audio recorder for capturing live sessions."""
from __future__ import annotations
import numpy as np
from datetime import datetime

class SessionRecorder:
    """Record live audio frames for later analysis or export."""

    def __init__(self, max_duration_s: float = 300.0, sr: int = 44100) -> None:
        self._sr = sr
        self._max_samples = int(max_duration_s * sr)
        self._chunks: list[np.ndarray] = []
        self._total_samples = 0
        self._started_at: datetime | None = None

    def start(self) -> None:
        self._started_at = datetime.now()
        self._chunks.clear()
        self._total_samples = 0

    def add_chunk(self, samples: np.ndarray) -> bool:
        if self._total_samples + len(samples) > self._max_samples:
            return False
        self._chunks.append(samples.astype(np.float32, copy=False))
        self._total_samples += len(samples)
        return True

    def get_recording(self) -> np.ndarray:
        if not self._chunks:
            return np.array([], dtype=np.float32)
        return np.concatenate(self._chunks)

    @property
    def duration_s(self) -> float:
        return self._total_samples / self._sr

    @property
    def is_recording(self) -> bool:
        return self._started_at is not None

    def stop(self) -> np.ndarray:
        recording = self.get_recording()
        self._started_at = None
        return recording
