"""Constellation-based fingerprinting (Shazam-inspired)."""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass

@dataclass
class Peak:
    time_idx: int
    freq_idx: int
    magnitude: float

@dataclass
class FingerprintHash:
    anchor_freq: int
    target_freq: int
    delta_time: int
    anchor_time: int

    @property
    def hash_value(self) -> int:
        return (self.anchor_freq << 20) | (self.target_freq << 10) | self.delta_time

class ConstellationFingerprinter:
    """Extract spectral peaks and create hash pairs for matching."""

    def __init__(self, fan_out: int = 10, target_zone: int = 50):
        self._fan_out = fan_out
        self._target_zone = target_zone

    def find_peaks(self, spectrogram: np.ndarray, threshold_db: float = -50) -> list[Peak]:
        peaks = []
        n_freq, n_time = spectrogram.shape
        for t in range(1, n_time - 1):
            for f in range(1, n_freq - 1):
                val = spectrogram[f, t]
                if val < threshold_db:
                    continue
                neighborhood = spectrogram[f-1:f+2, t-1:t+2]
                if val >= np.max(neighborhood):
                    peaks.append(Peak(time_idx=t, freq_idx=f, magnitude=float(val)))
        return peaks

    def generate_hashes(self, peaks: list[Peak]) -> list[FingerprintHash]:
        peaks.sort(key=lambda p: p.time_idx)
        hashes = []
        for i, anchor in enumerate(peaks):
            targets = [p for p in peaks[i+1:i+1+self._target_zone]
                      if p.time_idx > anchor.time_idx][:self._fan_out]
            for target in targets:
                hashes.append(FingerprintHash(
                    anchor_freq=anchor.freq_idx,
                    target_freq=target.freq_idx,
                    delta_time=target.time_idx - anchor.time_idx,
                    anchor_time=anchor.time_idx,
                ))
        return hashes
