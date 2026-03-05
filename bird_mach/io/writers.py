"""Audio writing utilities."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf


def save_wav(
    y: np.ndarray,
    path: Path,
    *,
    sr: int = 22050,
    subtype: str = "PCM_16",
) -> Path:
    """Write a waveform to a WAV file."""
    sf.write(str(path), y, sr, subtype=subtype)
    return path


def save_segment(
    y: np.ndarray,
    output_dir: Path,
    *,
    sr: int,
    index: int,
    prefix: str = "segment",
) -> Path:
    """Save a waveform segment with an indexed filename."""
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{prefix}_{index:04d}.wav"
    return save_wav(y, path, sr=sr)
