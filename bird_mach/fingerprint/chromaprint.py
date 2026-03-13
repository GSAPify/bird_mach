"""Simplified chromaprint-style audio fingerprinting."""
from __future__ import annotations
import hashlib
import numpy as np

class AudioFingerprinter:
    """Generate compact fingerprints from audio for similarity matching."""

    def __init__(self, sr: int = 22050, frame_size: int = 4096, hop: int = 2048):
        self._sr = sr
        self._frame_size = frame_size
        self._hop = hop

    def fingerprint(self, y: np.ndarray) -> str:
        n_frames = (len(y) - self._frame_size) // self._hop + 1
        if n_frames <= 0:
            return ""
        bits = []
        for i in range(n_frames):
            start = i * self._hop
            frame = y[start:start + self._frame_size]
            spectrum = np.abs(np.fft.rfft(frame))
            bands = [
                np.mean(spectrum[j:j+32])
                for j in range(0, min(256, len(spectrum)), 32)
            ]
            for j in range(len(bands) - 1):
                bits.append("1" if bands[j] > bands[j+1] else "0")
        bitstring = "".join(bits)
        return hashlib.sha256(bitstring.encode()).hexdigest()

    def similarity(self, fp1: str, fp2: str) -> float:
        if not fp1 or not fp2 or len(fp1) != len(fp2):
            return 0.0
        matches = sum(a == b for a, b in zip(fp1, fp2))
        return matches / len(fp1)
