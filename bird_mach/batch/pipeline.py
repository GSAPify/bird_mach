"""Configurable batch processing pipeline."""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class PipelineStep:
    name: str
    func: callable
    enabled: bool = True

@dataclass
class PipelineResult:
    path: Path
    success: bool
    outputs: dict = field(default_factory=dict)
    error: str | None = None

class BatchPipeline:
    """Run a configurable pipeline across many audio files."""

    def __init__(self):
        self._steps: list[PipelineStep] = []

    def add_step(self, name: str, func, enabled: bool = True) -> None:
        self._steps.append(PipelineStep(name=name, func=func, enabled=enabled))

    def process_file(self, path: Path) -> PipelineResult:
        outputs = {}
        for step in self._steps:
            if not step.enabled:
                continue
            try:
                outputs[step.name] = step.func(path, outputs)
            except Exception as e:
                logger.error("Step %s failed for %s: %s", step.name, path, e)
                return PipelineResult(path=path, success=False, error=str(e))
        return PipelineResult(path=path, success=True, outputs=outputs)

    def process_batch(self, paths: list[Path]) -> list[PipelineResult]:
        return [self.process_file(p) for p in paths]

    @property
    def step_count(self) -> int:
        return len(self._steps)
