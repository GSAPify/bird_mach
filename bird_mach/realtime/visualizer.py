"""Real-time visualization data formatter."""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass

@dataclass
class VisualizationFrame:
    """Formatted data ready for client-side rendering."""
    waveform: list[float]
    spectrum: list[float]
    bands: dict[str, float]
    rms: float
    peak: float
    centroid_hz: float
    is_onset: bool
    timestamp_ms: float

class VisualizationFormatter:
    """Transform raw analysis results into client-friendly payloads."""

    def __init__(self, waveform_points: int = 128, spectrum_points: int = 64):
        self._waveform_points = waveform_points
        self._spectrum_points = spectrum_points

    def format(self, raw: dict, waveform: np.ndarray) -> VisualizationFrame:
        wf = self._downsample(waveform, self._waveform_points)
        sp = raw.get("spectrum_db", [])[:self._spectrum_points]
        return VisualizationFrame(
            waveform=wf,
            spectrum=sp,
            bands=raw.get("bands", {}),
            rms=raw.get("rms", 0.0),
            peak=raw.get("peak", 0.0),
            centroid_hz=raw.get("centroid", 0.0),
            is_onset=raw.get("is_onset", False),
            timestamp_ms=raw.get("timestamp_ms", 0.0),
        )

    @staticmethod
    def _downsample(arr: np.ndarray, target: int) -> list[float]:
        if len(arr) <= target:
            return arr.tolist()
        indices = np.linspace(0, len(arr) - 1, target, dtype=int)
        return arr[indices].tolist()
