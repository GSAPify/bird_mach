"""Real-time loudness metering (simplified LUFS-style)."""
from __future__ import annotations
import numpy as np
from collections import deque

class LoudnessMeter:
    """Track short-term and integrated loudness."""

    def __init__(self, sr: int = 44100, window_s: float = 3.0):
        self._sr = sr
        self._window_samples = int(window_s * sr)
        self._history = deque(maxlen=100)
        self._integrated_sum = 0.0
        self._integrated_count = 0

    def process(self, samples: np.ndarray) -> dict[str, float]:
        rms = float(np.sqrt(np.mean(samples ** 2)))
        lufs_approx = 20 * np.log10(rms + 1e-10) - 0.691
        self._history.append(lufs_approx)
        self._integrated_sum += lufs_approx
        self._integrated_count += 1
        short_term = float(np.mean(list(self._history)[-10:])) if self._history else -70.0
        return {
            "momentary_lufs": lufs_approx,
            "short_term_lufs": short_term,
            "integrated_lufs": self._integrated_sum / max(self._integrated_count, 1),
            "peak_dbfs": float(20 * np.log10(np.max(np.abs(samples)) + 1e-10)),
        }
