"""Track dominant frequency over time."""
from __future__ import annotations
import numpy as np
from collections import deque

class FrequencyTracker:
    """Track the dominant frequency across consecutive frames."""

    def __init__(self, sr: int = 22050, history_size: int = 50):
        self._sr = sr
        self._history = deque(maxlen=history_size)

    def update(self, spectrum: np.ndarray) -> float:
        if len(spectrum) < 2:
            return 0.0
        peak_bin = int(np.argmax(spectrum[1:])) + 1
        freq = peak_bin * self._sr / (2 * (len(spectrum) - 1))
        self._history.append(freq)
        return freq

    @property
    def current(self) -> float:
        return self._history[-1] if self._history else 0.0

    @property
    def smoothed(self) -> float:
        if len(self._history) < 3:
            return self.current
        return float(np.median(list(self._history)[-5:]))

    @property
    def trend(self) -> str:
        if len(self._history) < 10:
            return "stable"
        recent = list(self._history)[-10:]
        slope = recent[-1] - recent[0]
        if slope > 50:
            return "rising"
        if slope < -50:
            return "falling"
        return "stable"
