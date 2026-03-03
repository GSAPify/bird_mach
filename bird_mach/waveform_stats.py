"""Waveform-level statistics for quick audio characterization."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class WaveformStats:
    """Summary statistics computed directly from the time-domain waveform."""

    peak: float
    rms: float
    crest_factor: float
    dynamic_range_db: float
    dc_offset: float
    zero_crossings: int
    duration_s: float
    sample_rate: int
    n_samples: int


def compute_waveform_stats(y: np.ndarray, *, sr: int) -> WaveformStats:
    """Compute time-domain statistics without spectral analysis."""
    peak = float(np.max(np.abs(y)))
    rms = float(np.sqrt(np.mean(y ** 2)))
    crest = peak / rms if rms > 1e-10 else 0.0
    dynamic_range = 20.0 * np.log10(peak / rms) if rms > 1e-10 else 0.0
    dc_offset = float(np.mean(y))
    zc = int(np.sum(np.abs(np.diff(np.sign(y))) > 0))

    return WaveformStats(
        peak=peak,
        rms=rms,
        crest_factor=crest,
        dynamic_range_db=float(dynamic_range),
        dc_offset=dc_offset,
        zero_crossings=zc,
        duration_s=len(y) / sr,
        sample_rate=sr,
        n_samples=len(y),
    )
