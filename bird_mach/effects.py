"""Audio effects and transformations."""

from __future__ import annotations

import numpy as np
import librosa


def change_speed(y: np.ndarray, *, rate: float) -> np.ndarray:
    """Time-stretch audio without changing pitch."""
    return librosa.effects.time_stretch(y, rate=rate)


def change_pitch(y: np.ndarray, *, sr: int, n_steps: float) -> np.ndarray:
    """Shift pitch by n semitones without changing tempo."""
    return librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)


def apply_fade(
    y: np.ndarray,
    *,
    sr: int,
    fade_in_s: float = 0.0,
    fade_out_s: float = 0.0,
) -> np.ndarray:
    """Apply linear fade-in and/or fade-out."""
    y = y.copy()
    if fade_in_s > 0:
        n = int(fade_in_s * sr)
        y[:n] *= np.linspace(0.0, 1.0, n, dtype=y.dtype)
    if fade_out_s > 0:
        n = int(fade_out_s * sr)
        y[-n:] *= np.linspace(1.0, 0.0, n, dtype=y.dtype)
    return y


def mix(y1: np.ndarray, y2: np.ndarray, *, ratio: float = 0.5) -> np.ndarray:
    """Mix two audio signals. ratio=0.5 means equal blend."""
    min_len = min(len(y1), len(y2))
    return (ratio * y1[:min_len] + (1.0 - ratio) * y2[:min_len]).astype(np.float32)
