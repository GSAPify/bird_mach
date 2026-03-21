"""Audio data augmentation for ML training."""
from __future__ import annotations
import numpy as np

def add_noise(y: np.ndarray, snr_db: float = 20.0) -> np.ndarray:
    rms_signal = np.sqrt(np.mean(y ** 2))
    rms_noise = rms_signal / (10 ** (snr_db / 20))
    noise = np.random.randn(len(y)).astype(y.dtype) * rms_noise
    return y + noise

def time_shift(y: np.ndarray, shift_max: int = 4410) -> np.ndarray:
    shift = np.random.randint(-shift_max, shift_max)
    return np.roll(y, shift)

def change_volume(y: np.ndarray, gain_db_range: tuple[float, float] = (-6, 6)) -> np.ndarray:
    gain_db = np.random.uniform(*gain_db_range)
    return y * (10 ** (gain_db / 20))

def time_mask(y: np.ndarray, max_mask: int = 2205) -> np.ndarray:
    out = y.copy()
    start = np.random.randint(0, max(1, len(y) - max_mask))
    length = np.random.randint(1, max_mask)
    out[start:start + length] = 0
    return out

def augment(y: np.ndarray) -> np.ndarray:
    y = add_noise(y, snr_db=np.random.uniform(15, 30))
    y = time_shift(y, shift_max=min(4410, len(y) // 4))
    y = change_volume(y)
    return y
