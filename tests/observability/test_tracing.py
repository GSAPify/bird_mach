"""Tests for distributed tracing."""
from bird_mach.observability.tracing import Tracer

class TestTracer:
    def test_start_trace(self):
        t = Tracer()
        span = t.start_trace("request")
        assert span.trace_id
        assert span.name == "request"

    def test_child_span(self):
        t = Tracer()
        root = t.start_trace("request")
        child = t.start_span("db_query", root)
        assert child.parent_id == root.span_id
        assert child.trace_id == root.trace_id

    def test_finish(self):
        t = Tracer()
        span = t.start_trace("request")
        span.finish()
        assert span.duration_ms >= 0

    def test_get_trace(self):
        t = Tracer()
        root = t.start_trace("request")
        t.start_span("child", root)
        trace = t.get_trace(root.trace_id)
        assert len(trace) == 2
