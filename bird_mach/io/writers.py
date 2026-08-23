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
    if sr <= 0:
        raise ValueError("sr must be positive")
    path.parent.mkdir(parents=True, exist_ok=True)
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
    # A prefix containing separators or ".." would escape output_dir.
    safe_prefix = Path(prefix).name
    if not safe_prefix or safe_prefix in {".", ".."}:
        raise ValueError(f"invalid segment prefix: {prefix!r}")
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{safe_prefix}_{index:04d}.wav"
    return save_wav(y, path, sr=sr)
