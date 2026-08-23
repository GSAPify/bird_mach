"""SDK data models."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class AnalysisResult:
    audio_id: str
    duration_s: float
    tempo_bpm: float
    key: str
    mode: str
    energy: float
    tags: list[str] = field(default_factory=list)

    @property
    def summary(self) -> str:
        return f"{self.key} {self.mode}, {self.tempo_bpm:.0f} BPM, {self.duration_s:.1f}s"

@dataclass
class SearchResult:
    audio_id: str
    title: str
    score: float
    metadata: dict = field(default_factory=dict)

@dataclass
class BatchResult:
    total: int
    completed: int
    failed: int
    results: list[AnalysisResult] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        if self.total <= 0:
            return 0.0
        return self.completed / self.total * 100
