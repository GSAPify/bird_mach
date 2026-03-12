"""Audio normalization utilities."""
from __future__ import annotations
import numpy as np

def peak_normalize(y: np.ndarray, target_db: float = -1.0) -> np.ndarray:
    peak = np.max(np.abs(y))
    if peak < 1e-10:
        return y
    target = 10 ** (target_db / 20)
    return y * (target / peak)

def rms_normalize(y: np.ndarray, target_db: float = -20.0) -> np.ndarray:
    rms = np.sqrt(np.mean(y ** 2))
    if rms < 1e-10:
        return y
    target = 10 ** (target_db / 20)
    return y * (target / rms)

def dc_remove(y: np.ndarray) -> np.ndarray:
    return y - np.mean(y)
