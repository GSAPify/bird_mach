"""Tests for PipelineContext."""
import pytest

import bird_mach.pipeline.context as context_mod
from bird_mach.pipeline.context import PipelineContext


def test_new_context_is_healthy():
    ctx = PipelineContext("p1")
    assert ctx.pipeline_id == "p1"
    assert ctx.is_healthy
    assert ctx.errors == []
