"""Distributed tracing support."""
from __future__ import annotations
import uuid
import time
from dataclasses import dataclass, field

@dataclass
class Span:
    trace_id: str
    span_id: str
    name: str
    parent_id: str | None = None
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    tags: dict[str, str] = field(default_factory=dict)
    status: str = "ok"

    def finish(self) -> None:
        self.end_time = time.time()

    @property
    def duration_ms(self) -> float:
        if self.end_time is None:
            return (time.time() - self.start_time) * 1000
        return (self.end_time - self.start_time) * 1000

class Tracer:
    def __init__(self):
        self._spans: list[Span] = []

    def start_trace(self, name: str) -> Span:
        span = Span(
            trace_id=str(uuid.uuid4())[:16],
            span_id=str(uuid.uuid4())[:8],
            name=name,
        )
        self._spans.append(span)
        return span

    def start_span(self, name: str, parent: Span) -> Span:
        span = Span(
            trace_id=parent.trace_id,
            span_id=str(uuid.uuid4())[:8],
            name=name,
            parent_id=parent.span_id,
        )
        self._spans.append(span)
        return span

    def get_trace(self, trace_id: str) -> list[Span]:
        return [s for s in self._spans if s.trace_id == trace_id]

    @property
    def total_spans(self) -> int:
        return len(self._spans)
