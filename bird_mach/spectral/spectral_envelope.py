"""Spectral envelope extraction via cepstral smoothing."""
from __future__ import annotations
import numpy as np

def spectral_envelope(spectrum: np.ndarray, n_cepstral: int = 30) -> np.ndarray:
    log_spectrum = np.log(np.abs(spectrum) + 1e-10)
    cepstrum = np.fft.ifft(log_spectrum).real
    liftered = np.zeros_like(cepstrum)
    liftered[:n_cepstral] = cepstrum[:n_cepstral]
    liftered[-n_cepstral + 1:] = cepstrum[-n_cepstral + 1:]
    return np.exp(np.fft.fft(liftered).real).astype(np.float32)

def spectral_tilt(spectrum: np.ndarray, sr: int) -> float:
    freqs = np.linspace(1, sr / 2, len(spectrum))
    log_freqs = np.log(freqs)
    log_mags = np.log(np.abs(spectrum) + 1e-10)
    coeffs = np.polyfit(log_freqs, log_mags, 1)
    return float(coeffs[0])
