"""Tests for AnalysisNode."""
from bird_mach.pipeline.nodes.analysis_node import AnalysisNode


def test_defaults_enable_both_features():
    assert AnalysisNode().process({}) == {"analyzed": True, "mfcc": True, "chroma": True}
