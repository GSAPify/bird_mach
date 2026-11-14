"""Tests for NormalizeNode."""
import pytest

from bird_mach.pipeline.nodes.normalize_node import NormalizeNode


def test_default_target_db():
    assert NormalizeNode().process({}) == {"normalized": True, "target_db": -1.0}
