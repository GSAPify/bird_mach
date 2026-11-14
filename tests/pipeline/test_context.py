"""Tests for PipelineContext."""
import pytest

import bird_mach.pipeline.context as context_mod
from bird_mach.pipeline.context import PipelineContext


def test_new_context_is_healthy():
    ctx = PipelineContext("p1")
    assert ctx.pipeline_id == "p1"
    assert ctx.is_healthy
    assert ctx.errors == []


def test_log_error_marks_context_unhealthy():
    ctx = PipelineContext("p1")
    ctx.log_error("disk full")
    assert not ctx.is_healthy
    assert ctx.errors == ["disk full"]


def test_errors_keep_insertion_order():
    ctx = PipelineContext("p1")
    for msg in ("a", "b", "c"):
        ctx.log_error(msg)
    assert ctx.errors == ["a", "b", "c"]
