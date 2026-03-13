"""Tests for spectral contrast."""
import numpy as np
from bird_mach.spectral.spectral_contrast import spectral_contrast

class TestSpectralContrast:
    def test_returns_bands(self):
        spectrum = np.random.rand(1025).astype(np.float32) * 10
        result = spectral_contrast(spectrum, sr=22050)
        assert "peaks" in result
        assert "valleys" in result
        assert "contrast" in result

    def test_contrast_non_negative(self):
        spectrum = np.abs(np.random.randn(1025).astype(np.float32))
        result = spectral_contrast(spectrum, sr=22050)
        assert np.all(result["contrast"] >= -0.01)
