"""Pipeline execution context with metadata tracking."""
from __future__ import annotations
import time
from dataclasses import dataclass, field

@dataclass
class PipelineContext:
    pipeline_id: str
    started_at: float = field(default_factory=time.time)
    metadata: dict = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    @property
    def elapsed_ms(self) -> float:
        return (time.time() - self.started_at) * 1000

    def log_error(self, msg: str) -> None:
        self.errors.append(msg)

    @property
    def is_healthy(self) -> bool:
        return len(self.errors) == 0
