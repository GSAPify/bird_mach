"""Real-time pitch tracking using autocorrelation."""
from __future__ import annotations
import numpy as np
from collections import deque

class RealtimePitchTracker:
    """Estimate pitch in real-time via autocorrelation."""

    def __init__(self, sr: int = 44100, fmin: float = 65.0, fmax: float = 2000.0):
        self._sr = sr
        self._min_lag = int(sr / fmax)
        self._max_lag = int(sr / fmin)
        self._history = deque(maxlen=30)

    def estimate(self, frame: np.ndarray) -> float:
        if len(frame) < self._max_lag:
            return 0.0
        corr = np.correlate(frame, frame, mode="full")
        corr = corr[len(corr) // 2:]
        search = corr[self._min_lag:self._max_lag]
        if len(search) == 0:
            return 0.0
        peak_idx = np.argmax(search) + self._min_lag
        if corr[peak_idx] < 0.1 * corr[0]:
            return 0.0
        freq = self._sr / peak_idx
        self._history.append(freq)
        return freq

    @property
    def smoothed_hz(self) -> float:
        if len(self._history) < 3:
            return 0.0
        return float(np.median(list(self._history)))
