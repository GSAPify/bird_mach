"""Audio file loading with format detection and validation."""

from __future__ import annotations

import logging
from pathlib import Path

import librosa
import numpy as np

from bird_mach.constants import SUPPORTED_AUDIO_EXTENSIONS, MAX_AUDIO_DURATION_S
from bird_mach.exceptions import AudioLoadError, AudioTooLongError

logger = logging.getLogger(__name__)


def load_audio(
    path: Path,
    *,
    sr: int = 22050,
    mono: bool = True,
    max_duration_s: float | None = None,
) -> tuple[np.ndarray, int]:
    """Load an audio file with validation.

    Raises AudioLoadError if the file can't be decoded,
    AudioTooLongError if it exceeds the duration limit.
    """
    if not path.exists():
        raise AudioLoadError(f"File not found: {path}")

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_AUDIO_EXTENSIONS:
        raise AudioLoadError(f"Unsupported format: {suffix}")

    try:
        duration = librosa.get_duration(path=str(path))
    except Exception as exc:
        raise AudioLoadError(f"Cannot read audio metadata: {exc}") from exc

    limit = max_duration_s or MAX_AUDIO_DURATION_S
    if duration > limit:
        raise AudioTooLongError(duration, limit)

    logger.info("Loading %s (%.1fs, target sr=%d)", path.name, duration, sr)
    y, actual_sr = librosa.load(str(path), sr=sr, mono=mono)
    return y.astype(np.float32, copy=False), actual_sr


def load_audio_bytes(
    data: bytes,
    *,
    suffix: str = ".wav",
    sr: int = 22050,
) -> tuple[np.ndarray, int]:
    """Load audio from raw bytes via a temp file."""
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as tmp:
        tmp.write(data)
        tmp.flush()
        return load_audio(Path(tmp.name), sr=sr)
