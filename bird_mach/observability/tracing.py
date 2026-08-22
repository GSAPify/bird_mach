"""Distributed tracing support."""
from __future__ import annotations
import uuid
import time
from collections import deque
from dataclasses import dataclass, field

@dataclass
class Span:
    trace_id: str
    span_id: str
    name: str
    parent_id: str | None = None
    start_time: float = field(default_factory=time.monotonic)
    end_time: float | None = None
    tags: dict[str, str] = field(default_factory=dict)
    status: str = "ok"

    def finish(self) -> None:
        if self.end_time is None:
            self.end_time = time.monotonic()

    @property
    def duration_ms(self) -> float:
        end = self.end_time if self.end_time is not None else time.monotonic()
        return (end - self.start_time) * 1000

class Tracer:
    def __init__(self, max_spans: int = 10000):
        if max_spans < 1:
            raise ValueError("max_spans must be at least 1")
        self._spans: deque[Span] = deque(maxlen=max_spans)

    def start_trace(self, name: str) -> Span:
        span = Span(
            trace_id=uuid.uuid4().hex,
            span_id=uuid.uuid4().hex,
            name=name,
        )
        self._spans.append(span)
        return span

    def start_span(self, name: str, parent: Span) -> Span:
        span = Span(
            trace_id=parent.trace_id,
            span_id=uuid.uuid4().hex,
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
