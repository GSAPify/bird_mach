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


def test_node_result_carries_error():
    result = NodeResult("loader", False, {}, duration_ms=3.5, error="boom")
    assert not result.success
    assert result.error == "boom"
    assert result.duration_ms == 3.5


def test_builtin_nodes_match_protocol_shape():
    for node in (LoaderNode(), NormalizeNode(), AnalysisNode(), ExportNode()):
        assert isinstance(node.name, str) and node.name
        assert callable(node.process)
