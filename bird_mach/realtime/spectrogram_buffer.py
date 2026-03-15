"""Rolling spectrogram buffer for live visualization."""
from __future__ import annotations
import numpy as np

class SpectrogramBuffer:
    """Maintain a rolling 2D spectrogram for real-time display."""

    def __init__(self, n_frames: int = 200, n_bins: int = 128):
        self._buffer = np.full((n_bins, n_frames), -80.0, dtype=np.float32)
        self._n_frames = n_frames
        self._n_bins = n_bins
        self._pos = 0

    def push(self, spectrum_db: np.ndarray) -> None:
        col = spectrum_db[:self._n_bins] if len(spectrum_db) >= self._n_bins else np.pad(
            spectrum_db, (0, self._n_bins - len(spectrum_db)), constant_values=-80
        )
        self._buffer[:, self._pos % self._n_frames] = col
        self._pos += 1

    def get_image(self) -> np.ndarray:
        if self._pos <= self._n_frames:
            return self._buffer[:, :self._pos]
        start = self._pos % self._n_frames
        return np.hstack([self._buffer[:, start:], self._buffer[:, :start]])

    @property
    def frame_count(self) -> int:
        return self._pos
