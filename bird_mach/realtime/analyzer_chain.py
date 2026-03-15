"""Chain multiple real-time analyzers together."""
from __future__ import annotations
import numpy as np
from typing import Protocol

class RealtimeAnalyzer(Protocol):
    def analyze(self, samples: np.ndarray, sr: int) -> dict: ...

class AnalyzerChain:
    """Run multiple analyzers on each audio frame."""
    def __init__(self):
        self._analyzers: list[tuple[str, RealtimeAnalyzer]] = []

    def add(self, name: str, analyzer: RealtimeAnalyzer) -> None:
        self._analyzers.append((name, analyzer))

    def process(self, samples: np.ndarray, sr: int) -> dict:
        results = {}
        for name, analyzer in self._analyzers:
            results[name] = analyzer.analyze(samples, sr)
        return results

    @property
    def analyzer_count(self) -> int:
        return len(self._analyzers)
