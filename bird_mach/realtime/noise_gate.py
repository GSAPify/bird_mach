"""Real-time noise gate."""
from __future__ import annotations
import numpy as np

class NoiseGate:
    """Simple noise gate that mutes signal below a threshold."""
    def __init__(self, threshold_db: float = -40.0, attack_ms: float = 1.0, release_ms: float = 50.0):
        self._threshold = 10 ** (threshold_db / 20)
        self._attack = attack_ms
        self._release = release_ms
        self._open = False

    def process(self, samples: np.ndarray) -> np.ndarray:
        rms = float(np.sqrt(np.mean(samples ** 2)))
        if rms > self._threshold:
            self._open = True
        elif rms < self._threshold * 0.7:
            self._open = False
        return samples if self._open else samples * 0.01

    @property
    def is_open(self) -> bool:
        return self._open
