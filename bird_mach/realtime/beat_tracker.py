"""Real-time beat detection for live audio."""
from __future__ import annotations
import numpy as np
from collections import deque

class RealtimeBeatTracker:
    """Detect beats in real-time using onset strength peaks."""

    def __init__(self, sr: int = 44100, hop_length: int = 512) -> None:
        self._sr = sr
        self._hop = hop_length
        self._onset_history = deque(maxlen=200)
        self._beat_times: list[float] = []
        self._threshold = 0.0
        self._cooldown = 0

    def process(self, spectrum: np.ndarray, timestamp_s: float) -> bool:
        onset_strength = float(np.sum(np.maximum(0, np.diff(spectrum))))
        self._onset_history.append(onset_strength)

        if len(self._onset_history) < 10:
            return False

        self._threshold = np.mean(list(self._onset_history)) * 1.4 + 0.01

        if self._cooldown > 0:
            self._cooldown -= 1
            return False

        if onset_strength > self._threshold:
            self._beat_times.append(timestamp_s)
            self._cooldown = 8
            return True
        return False

    @property
    def bpm(self) -> float:
        if len(self._beat_times) < 3:
            return 0.0
        intervals = np.diff(self._beat_times[-20:])
        mean_interval = float(np.median(intervals))
        if mean_interval <= 0:
            return 0.0
        return 60.0 / mean_interval

    @property
    def beat_count(self) -> int:
        return len(self._beat_times)
