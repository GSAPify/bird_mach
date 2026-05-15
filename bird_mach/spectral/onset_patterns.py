"""Onset pattern analysis for rhythm characterization."""
from __future__ import annotations
import numpy as np

def compute_onset_pattern(onset_times: np.ndarray, window_s: float = 4.0) -> dict:
    if len(onset_times) < 3:
        return {"regularity": 0.0, "density": 0.0, "mean_interval_s": 0.0, "intervals": []}
    intervals = np.diff(onset_times)
    mean_int = float(np.mean(intervals))
    std_int = float(np.std(intervals))
    regularity = 1.0 - min(std_int / (mean_int + 1e-10), 1.0)
    density = len(onset_times) / max(onset_times[-1] - onset_times[0], 1e-10)
    return {
        "regularity": round(regularity, 3),
        "density": round(density, 2),
        "mean_interval_s": round(mean_int, 4),
        "intervals": intervals.tolist(),
    }

def classify_rhythm(regularity: float, density: float) -> str:
    if regularity > 0.8 and density > 3:
        return "metronomic"
    if regularity > 0.6:
        return "steady"
    if density > 5:
        return "busy"
    if density < 1:
        return "sparse"
    return "freeform"
