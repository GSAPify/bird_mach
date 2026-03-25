"""Tests for harmonic ratio."""
import numpy as np
from bird_mach.spectral.harmonic_ratio import harmonic_noise_ratio

class TestHarmonicRatio:
    def test_pure_tone(self):
        sr = 22050
        t = np.linspace(0, 1, sr)
        y = np.sin(2 * np.pi * 440 * t).astype(np.float32)
        hnr = harmonic_noise_ratio(y, sr)
        assert hnr > 5.0

    def test_noise(self):
        sr = 22050
        y = np.random.randn(sr).astype(np.float32)
        hnr = harmonic_noise_ratio(y, sr)
        assert hnr < 20.0
