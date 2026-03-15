"""Dynamic range analysis for real-time audio."""
from __future__ import annotations
import numpy as np
from collections import deque

class DynamicsAnalyzer:
    """Track dynamic range statistics over a sliding window."""
    def __init__(self, window_size: int = 100):
        self._peaks = deque(maxlen=window_size)
        self._rms_vals = deque(maxlen=window_size)

    def update(self, samples: np.ndarray) -> dict:
        peak = float(np.max(np.abs(samples)))
        rms = float(np.sqrt(np.mean(samples**2)))
        self._peaks.append(peak)
        self._rms_vals.append(rms)
        crest = peak / (rms + 1e-10)
        dr = 20 * np.log10(max(self._peaks) / (np.mean(list(self._rms_vals)) + 1e-10))
        return {"peak": peak, "rms": rms, "crest_factor": crest, "dynamic_range_db": float(dr)}
