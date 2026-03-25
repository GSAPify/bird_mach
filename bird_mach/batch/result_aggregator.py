"""Aggregate results from batch processing runs."""
from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np

@dataclass
class BatchSummary:
    total_files: int = 0
    successful: int = 0
    failed: int = 0
    total_duration_s: float = 0.0
    avg_rms: float = 0.0
    avg_tempo: float = 0.0
    format_counts: dict[str, int] = field(default_factory=dict)

class ResultAggregator:
    def __init__(self):
        self._rms_vals: list[float] = []
        self._tempos: list[float] = []
        self._formats: dict[str, int] = {}
        self._success = 0
        self._fail = 0
        self._duration = 0.0

    def add(self, result: dict, format: str = "wav") -> None:
        self._success += 1
        self._rms_vals.append(result.get("rms", 0))
        self._tempos.append(result.get("tempo", 0))
        self._duration += result.get("duration_s", 0)
        self._formats[format] = self._formats.get(format, 0) + 1

    def add_failure(self) -> None:
        self._fail += 1

    def summarize(self) -> BatchSummary:
        return BatchSummary(
            total_files=self._success + self._fail,
            successful=self._success, failed=self._fail,
            total_duration_s=self._duration,
            avg_rms=float(np.mean(self._rms_vals)) if self._rms_vals else 0.0,
            avg_tempo=float(np.mean(self._tempos)) if self._tempos else 0.0,
            format_counts=dict(self._formats),
        )
