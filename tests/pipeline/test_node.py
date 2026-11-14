"""Tests for the pipeline node abstractions."""
from bird_mach.pipeline.node import NodeResult
from bird_mach.pipeline.nodes.analysis_node import AnalysisNode
from bird_mach.pipeline.nodes.export_node import ExportNode
from bird_mach.pipeline.nodes.loader_node import LoaderNode
from bird_mach.pipeline.nodes.normalize_node import NormalizeNode


def test_node_result_defaults():
    result = NodeResult("loader", True, {"a": 1})
    assert result.duration_ms == 0.0
    assert result.error is None
