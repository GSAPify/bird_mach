"""Tests for AnalysisNode."""
from bird_mach.pipeline.nodes.analysis_node import AnalysisNode


def test_defaults_enable_both_features():
    assert AnalysisNode().process({}) == {"analyzed": True, "mfcc": True, "chroma": True}


def test_features_can_be_disabled():
    out = AnalysisNode(compute_mfcc=False, compute_chroma=False).process({})
    assert out == {"analyzed": True, "mfcc": False, "chroma": False}


def test_process_ignores_input_data():
    assert AnalysisNode().process({"x": 1}) == AnalysisNode().process({})
