"""Phase vocoder for time-stretching without pitch change."""
from __future__ import annotations
import numpy as np


class PhaseVocoder:
    """Time-stretch audio using phase vocoder technique."""

    def __init__(self, n_fft: int = 2048, hop_length: int = 512):
        self._n_fft = n_fft
        self._hop = hop_length

    def time_stretch(self, y: np.ndarray, rate: float) -> np.ndarray:
        """Stretch audio by `rate` (>1 = faster, <1 = slower)."""
        stft = self._stft(y)
        stretched = self._stretch_stft(stft, rate)
        return self._istft(stretched)

    def _stft(self, y: np.ndarray) -> np.ndarray:
        window = np.hanning(self._n_fft)
        n_frames = (len(y) - self._n_fft) // self._hop + 1
        result = np.zeros((self._n_fft // 2 + 1, n_frames), dtype=complex)
        for i in range(n_frames):
            start = i * self._hop
            frame = y[start:start + self._n_fft] * window
            result[:, i] = np.fft.rfft(frame)
        return result

    def _stretch_stft(self, stft: np.ndarray, rate: float) -> np.ndarray:
        n_bins, n_frames = stft.shape
        new_n = int(n_frames / rate)
        phases = np.angle(stft)
        magnitudes = np.abs(stft)
        result = np.zeros((n_bins, new_n), dtype=complex)
        for i in range(new_n):
            src = i * rate
            idx = int(src)
            frac = src - idx
            if idx + 1 < n_frames:
                mag = (1 - frac) * magnitudes[:, idx] + frac * magnitudes[:, idx + 1]
                ph = phases[:, idx]
            elif idx < n_frames:
                mag = magnitudes[:, idx]
                ph = phases[:, idx]
            else:
                break
            result[:, i] = mag * np.exp(1j * ph)
        return result

    def _istft(self, stft: np.ndarray) -> np.ndarray:
        n_bins, n_frames = stft.shape
        window = np.hanning(self._n_fft)
        length = self._n_fft + (n_frames - 1) * self._hop
        y = np.zeros(length)
        window_sum = np.zeros(length)
        for i in range(n_frames):
            start = i * self._hop
            frame = np.fft.irfft(stft[:, i])[:self._n_fft] * window
            y[start:start + self._n_fft] += frame
            window_sum[start:start + self._n_fft] += window ** 2
        nonzero = window_sum > 1e-10
        y[nonzero] /= window_sum[nonzero]
        return y.astype(np.float32)
