"""Compare two audio analysis summaries side by side."""

from __future__ import annotations

from dataclasses import dataclass

from bird_mach.analysis import AnalysisSummary


@dataclass
class ComparisonResult:
    """Side-by-side comparison of two audio summaries."""

    a: AnalysisSummary
    b: AnalysisSummary

    @property
    def tempo_diff(self) -> float:
        return self.b.tempo_bpm - self.a.tempo_bpm

    @property
    def energy_diff(self) -> float:
        return self.b.rms_mean - self.a.rms_mean

    @property
    def brightness_diff(self) -> float:
        return self.b.spectral_centroid_mean - self.a.spectral_centroid_mean

    @property
    def duration_diff(self) -> float:
        return self.b.duration_s - self.a.duration_s

    def to_dict(self) -> dict[str, dict[str, float]]:
        """Return a dictionary suitable for tabular display."""
        fields = [
            "duration_s", "tempo_bpm", "rms_mean", "rms_max",
            "spectral_centroid_mean", "spectral_bandwidth_mean",
            "zero_crossing_rate_mean", "onset_count",
        ]
        result: dict[str, dict[str, float]] = {}
        for f in fields:
            va = getattr(self.a, f)
            vb = getattr(self.b, f)
            result[f] = {"a": float(va), "b": float(vb), "diff": float(vb - va)}
        return result


def compare(a: AnalysisSummary, b: AnalysisSummary) -> ComparisonResult:
    """Create a comparison between two analysis summaries."""
    return ComparisonResult(a=a, b=b)
