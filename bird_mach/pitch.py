"""Pitch detection utilities for audio analysis."""

from __future__ import annotations

from dataclasses import dataclass

import librosa
import numpy as np


@dataclass
class PitchResult:
    """Result of pitch estimation."""

    f0: np.ndarray
    voiced_flag: np.ndarray
    times_s: np.ndarray
    median_hz: float
    confidence: float


def estimate_pitch(
    y: np.ndarray,
    *,
    sr: int,
    fmin: float = 65.0,
    fmax: float = 2093.0,
    hop_length: int = 512,
) -> PitchResult:
    """Estimate fundamental frequency using pyin.

    Args:
        y: Audio waveform (mono, float32).
        sr: Sample rate.
        fmin: Minimum expected frequency (default C2).
        fmax: Maximum expected frequency (default C7).
    """
    f0, voiced, _ = librosa.pyin(
        y, fmin=fmin, fmax=fmax, sr=sr, hop_length=hop_length
    )
    times = librosa.times_like(f0, sr=sr, hop_length=hop_length)

    voiced_f0 = f0[voiced]
    median_hz = float(np.median(voiced_f0)) if len(voiced_f0) > 0 else 0.0
    confidence = float(np.mean(voiced))

    return PitchResult(
        f0=np.nan_to_num(f0).astype(np.float32),
        voiced_flag=voiced.astype(np.bool_),
        times_s=times.astype(np.float32),
        median_hz=median_hz,
        confidence=confidence,
    )


def hz_to_note(freq_hz: float) -> str:
    """Convert a frequency in Hz to the nearest musical note name."""
    if freq_hz <= 0:
        return "—"
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    midi = 12 * np.log2(freq_hz / 440.0) + 69
    midi_round = int(round(midi))
    octave = (midi_round // 12) - 1
    note = note_names[midi_round % 12]
    return f"{note}{octave}"
