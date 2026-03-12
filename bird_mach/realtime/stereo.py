"""Stereo analysis utilities."""
from __future__ import annotations
import numpy as np

def compute_stereo_width(left: np.ndarray, right: np.ndarray) -> float:
    mid = (left + right) / 2
    side = (left - right) / 2
    mid_rms = np.sqrt(np.mean(mid**2)) + 1e-10
    side_rms = np.sqrt(np.mean(side**2))
    return float(side_rms / mid_rms)

def compute_correlation(left: np.ndarray, right: np.ndarray) -> float:
    if len(left) != len(right):
        return 0.0
    corr = np.corrcoef(left, right)[0, 1]
    return float(corr) if not np.isnan(corr) else 0.0

def pan_position(left: np.ndarray, right: np.ndarray) -> float:
    l_rms = np.sqrt(np.mean(left**2))
    r_rms = np.sqrt(np.mean(right**2))
    total = l_rms + r_rms + 1e-10
    return float((r_rms - l_rms) / total)
