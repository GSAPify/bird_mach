"""Digital signal processing utilities for real-time analysis."""
from __future__ import annotations
import numpy as np

def compute_fft_bands(
    spectrum: np.ndarray,
    sr: int,
    bands: list[tuple[float, float]] | None = None,
) -> dict[str, float]:
    """Compute energy in frequency bands from an FFT spectrum."""
    if bands is None:
        bands = [
            (20, 60), (60, 250), (250, 500), (500, 2000),
            (2000, 4000), (4000, 8000), (8000, 16000),
        ]
    band_names = ["sub", "bass", "low_mid", "mid", "high_mid", "presence", "brilliance"]
    n_bins = len(spectrum)
    freqs = np.linspace(0, sr / 2, n_bins)
    result = {}
    for name, (lo, hi) in zip(band_names, bands):
        mask = (freqs >= lo) & (freqs < hi)
        energy = float(np.mean(spectrum[mask] ** 2)) if mask.any() else 0.0
        result[name] = energy
    return result

def apply_window(samples: np.ndarray, window: str = "hann") -> np.ndarray:
    """Apply a windowing function to a frame of samples."""
    n = len(samples)
    if window == "hann":
        w = np.hanning(n)
    elif window == "hamming":
        w = np.hamming(n)
    elif window == "blackman":
        w = np.blackman(n)
    else:
        w = np.ones(n)
    return samples * w

def compute_spectral_flux(prev: np.ndarray, curr: np.ndarray) -> float:
    """Compute spectral flux between consecutive frames."""
    diff = curr - prev
    return float(np.sum(diff[diff > 0] ** 2))

def detect_onset_realtime(
    flux_history: list[float], threshold_ratio: float = 1.5
) -> bool:
    """Simple onset detection based on spectral flux spike."""
    if len(flux_history) < 10:
        return False
    mean_flux = np.mean(flux_history[-10:])
    return flux_history[-1] > mean_flux * threshold_ratio

def mel_filterbank(sr: int, n_fft: int, n_mels: int = 40) -> np.ndarray:
    """Create a mel-scale filterbank matrix."""
    f_min, f_max = 0.0, sr / 2.0
    mel_min = 2595 * np.log10(1 + f_min / 700)
    mel_max = 2595 * np.log10(1 + f_max / 700)
    mel_points = np.linspace(mel_min, mel_max, n_mels + 2)
    hz_points = 700 * (10 ** (mel_points / 2595) - 1)
    bins = np.floor((n_fft + 1) * hz_points / sr).astype(int)
    fb = np.zeros((n_mels, n_fft // 2 + 1))
    for i in range(n_mels):
        for j in range(bins[i], bins[i + 1]):
            if j < fb.shape[1]:
                fb[i, j] = (j - bins[i]) / max(bins[i + 1] - bins[i], 1)
        for j in range(bins[i + 1], bins[i + 2]):
            if j < fb.shape[1]:
                fb[i, j] = (bins[i + 2] - j) / max(bins[i + 2] - bins[i + 1], 1)
    return fb
