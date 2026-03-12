"""Tests for real-time DSP utilities."""
import numpy as np
from bird_mach.realtime.dsp import (
    compute_fft_bands, apply_window, compute_spectral_flux,
    detect_onset_realtime, mel_filterbank,
)

class TestFFTBands:
    def test_returns_all_bands(self):
        spectrum = np.random.rand(2049).astype(np.float32)
        bands = compute_fft_bands(spectrum, sr=44100)
        assert len(bands) == 7
        assert "sub" in bands
        assert "brilliance" in bands

    def test_silence_is_zero(self):
        spectrum = np.zeros(2049)
        bands = compute_fft_bands(spectrum, sr=44100)
        assert all(v == 0.0 for v in bands.values())

class TestApplyWindow:
    def test_hann(self):
        x = np.ones(1024)
        windowed = apply_window(x, "hann")
        assert windowed[0] < 0.01
        assert windowed[512] > 0.99

    def test_identity(self):
        x = np.ones(1024)
        result = apply_window(x, "rect")
        assert np.allclose(result, x)

class TestSpectralFlux:
    def test_identical_is_zero(self):
        s = np.ones(100)
        assert compute_spectral_flux(s, s) == 0.0

class TestMelFilterbank:
    def test_shape(self):
        fb = mel_filterbank(sr=22050, n_fft=2048, n_mels=40)
        assert fb.shape == (40, 1025)
