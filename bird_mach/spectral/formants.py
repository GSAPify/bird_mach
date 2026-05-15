"""Formant frequency estimation for speech analysis."""
from __future__ import annotations
import numpy as np

def estimate_formants(y: np.ndarray, sr: int, n_formants: int = 4) -> list[float]:
    if len(y) == 0:
        return []
    order = 2 + n_formants * 2
    pre_emph = np.append(y[0], y[1:] - 0.97 * y[:-1])
    windowed = pre_emph[:2048] * np.hamming(min(len(pre_emph), 2048))
    if len(windowed) < order + 1:
        return []
    autocorr = np.correlate(windowed, windowed, "full")
    autocorr = autocorr[len(autocorr) // 2:][:order + 1]
    try:
        coeffs = np.linalg.solve(
            np.array([[autocorr[abs(i - j)] for j in range(order)]
                      for i in range(order)]),
            -autocorr[1:order + 1],
        )
    except np.linalg.LinAlgError:
        return []
    poly = np.concatenate([[1], coeffs])
    roots = np.roots(poly)
    roots = roots[np.imag(roots) > 0]
    angles = np.arctan2(np.imag(roots), np.real(roots))
    formant_freqs = sorted(angles * sr / (2 * np.pi))
    return [f for f in formant_freqs if 90 < f < sr / 2][:n_formants]
