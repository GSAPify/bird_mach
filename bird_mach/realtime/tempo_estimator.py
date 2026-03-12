"""Real-time tempo estimation via autocorrelation of onset envelope."""
from __future__ import annotations
import numpy as np
from collections import deque

class TempoEstimator:
    """Estimate tempo from streaming onset strength values."""
    def __init__(self, sr: int = 44100, hop: int = 512):
        self._sr = sr
        self._hop = hop
        self._onset_buf = deque(maxlen=500)

    def feed(self, onset_strength: float) -> None:
        self._onset_buf.append(onset_strength)

    @property
    def bpm(self) -> float:
        if len(self._onset_buf) < 100:
            return 0.0
        data = np.array(self._onset_buf)
        corr = np.correlate(data, data, mode="full")
        corr = corr[len(corr)//2:]
        bpm_min, bpm_max = 60, 200
        min_lag = int(60 * self._sr / (self._hop * bpm_max))
        max_lag = int(60 * self._sr / (self._hop * bpm_min))
        search = corr[min_lag:max_lag]
        if len(search) == 0:
            return 0.0
        best_lag = np.argmax(search) + min_lag
        return 60 * self._sr / (self._hop * best_lag)
