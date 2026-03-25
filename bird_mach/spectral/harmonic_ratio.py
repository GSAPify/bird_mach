"""Harmonic-to-noise ratio estimation."""
from __future__ import annotations
import numpy as np

def harmonic_noise_ratio(y: np.ndarray, sr: int, frame_size: int = 2048) -> float:
    spectrum = np.abs(np.fft.rfft(y[:frame_size]))
    freqs = np.fft.rfftfreq(frame_size, 1.0 / sr)
    if len(spectrum) < 10:
        return 0.0
    peak_idx = np.argmax(spectrum[1:]) + 1
    f0 = freqs[peak_idx]
    if f0 <= 0:
        return 0.0
    harmonic_energy = 0.0
    noise_energy = 0.0
    for i, (f, mag) in enumerate(zip(freqs, spectrum)):
        if f <= 0:
            continue
        ratio = f / f0
        if abs(ratio - round(ratio)) < 0.05:
            harmonic_energy += mag ** 2
        else:
            noise_energy += mag ** 2
    if noise_energy < 1e-10:
        return 100.0
    return 10 * np.log10(harmonic_energy / noise_energy)
