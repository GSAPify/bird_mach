"""Audio normalization utilities."""
from __future__ import annotations
import numpy as np

def peak_normalize(y: np.ndarray, target_db: float = -1.0) -> np.ndarray:
    if y.size == 0:
        return y
    peak = np.max(np.abs(y))
    # Same guard as rms_normalize: one NaN sample would otherwise NaN the whole signal.
    if not np.isfinite(peak) or peak < 1e-10:
        return y
    target = 10 ** (target_db / 20)
    return y * (target / peak)

def rms_normalize(y: np.ndarray, target_db: float = -20.0) -> np.ndarray:
    if y.size == 0:
        return y
    rms = np.sqrt(np.mean(y ** 2))
    # NaN fails the < comparison, so check finiteness explicitly.
    if not np.isfinite(rms) or rms < 1e-10:
        return y
    target = 10 ** (target_db / 20)
    return y * (target / rms)

def dc_remove(y: np.ndarray) -> np.ndarray:
    return y - np.mean(y)
