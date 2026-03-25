"""Spectral contrast for timbral analysis."""
from __future__ import annotations
import numpy as np

def spectral_contrast(
    spectrum: np.ndarray, sr: int, n_bands: int = 6, alpha: float = 0.02,
) -> dict[str, np.ndarray]:
    n_bins = len(spectrum)
    freqs = np.linspace(0, sr / 2, n_bins)
    edges = [0] + [200 * (2 ** i) for i in range(n_bands)] + [sr / 2]
    peaks = []
    valleys = []
    for i in range(len(edges) - 1):
        mask = (freqs >= edges[i]) & (freqs < edges[i + 1])
        band = spectrum[mask]
        if len(band) == 0:
            peaks.append(0.0)
            valleys.append(0.0)
            continue
        sorted_band = np.sort(band)
        n_alpha = max(1, int(len(sorted_band) * alpha))
        peaks.append(float(np.mean(sorted_band[-n_alpha:])))
        valleys.append(float(np.mean(sorted_band[:n_alpha])))
    return {
        "peaks": np.array(peaks),
        "valleys": np.array(valleys),
        "contrast": np.array(peaks) - np.array(valleys),
    }
