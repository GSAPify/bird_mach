"""Lightweight audio utility helpers — duration, format detection, normalization."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import librosa
import numpy as np
import soundfile as sf


@dataclass(frozen=True)
class AudioInfo:
    """Quick metadata about an audio file without loading the full waveform."""

    path: Path
    duration_s: float
    sample_rate: int
    channels: int

    @property
    def size_mb(self) -> float:
        return self.path.stat().st_size / (1024 * 1024) if self.path.exists() else 0.0


def probe_audio(path: Path, *, sr: int | None = None) -> AudioInfo:
    """Return basic metadata for an audio file."""
    duration = librosa.get_duration(path=str(path))
    file_info = sf.info(str(path))
    return AudioInfo(
        path=path,
        duration_s=duration,
        sample_rate=sr or file_info.samplerate,
        channels=file_info.channels,
    )


def normalize_waveform(y: np.ndarray) -> np.ndarray:
    """Peak-normalize a waveform to [-1, 1]."""
    if y.size == 0:
        return y
    peak = np.max(np.abs(y))
    if peak < 1e-8:
        return y
    return y / peak


def trim_silence(
    y: np.ndarray, *, sr: int, top_db: float = 30.0
) -> tuple[np.ndarray, int, int]:
    """Trim leading/trailing silence. Returns (trimmed, start_sample, end_sample)."""
    trimmed, idx = librosa.effects.trim(y, top_db=top_db)
    return trimmed, int(idx[0]), int(idx[1])
