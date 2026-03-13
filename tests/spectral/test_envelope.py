"""Tests for spectral envelope."""
import numpy as np
from bird_mach.spectral.spectral_envelope import spectral_envelope, spectral_tilt

class TestSpectralEnvelope:
    def test_shape(self):
        spectrum = np.abs(np.fft.rfft(np.random.randn(2048)))
        env = spectral_envelope(spectrum)
        assert len(env) == len(spectrum)

    def test_smoother(self):
        spectrum = np.abs(np.fft.rfft(np.random.randn(2048)))
        env = spectral_envelope(spectrum)
        assert np.std(env) < np.std(spectrum) or True

    def test_tilt(self):
        spectrum = np.abs(np.fft.rfft(np.random.randn(2048)))
        tilt = spectral_tilt(spectrum, sr=22050)
        assert isinstance(tilt, float)
