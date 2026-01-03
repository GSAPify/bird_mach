"""High-level audio analysis pipeline for Mach.

Provides composable analysis functions that build on top of the
low-level feature extraction in `embedding.py`. Each function returns
plain numpy arrays or dataclasses for easy downstream consumption.
"""

from __future__ import annotations

from dataclasses import dataclass

import librosa
import numpy as np


@dataclass
class OnsetResult:
    """Result of onset detection."""

    times_s: np.ndarray
    strengths: np.ndarray
    count: int

    @property
    def mean_interval_s(self) -> float:
        if self.count < 2:
            return 0.0
        return float(np.mean(np.diff(self.times_s)))


def detect_onsets(
    y: np.ndarray, *, sr: int, hop_length: int = 512
) -> OnsetResult:
    """Detect note onsets and return their timestamps and strengths."""
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    onset_frames = librosa.onset.onset_detect(
        onset_envelope=onset_env, sr=sr, hop_length=hop_length
    )
    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=hop_length)
    strengths = onset_env[onset_frames] if len(onset_frames) > 0 else np.array([])
    return OnsetResult(
        times_s=onset_times,
        strengths=strengths.astype(np.float32, copy=False),
        count=len(onset_frames),
    )
