"""Tests for pipeline graph."""
from bird_mach.pipeline.graph import PipelineGraph

class FakeNode:
    def __init__(self, name, output):
        self.name = name
        self._output = output
    def process(self, data):
        return self._output

class TestPipelineGraph:
    def test_single_node(self):
        g = PipelineGraph()
        g.add_node("a", FakeNode("a", {"result": 1}))
        results = g.execute({})
        assert results[0].success
        assert results[0].output == {"result": 1}

    def test_chain(self):
        g = PipelineGraph()
        g.add_node("a", FakeNode("a", {"x": 1}))
        g.add_node("b", FakeNode("b", {"y": 2}))
        g.add_edge("a", "b")
        results = g.execute({})
        assert len(results) == 2

    def test_failure(self):
        class FailNode:
            name = "fail"
            def process(self, data): raise ValueError("boom")
        g = PipelineGraph()
        g.add_node("f", FailNode())
        results = g.execute({})
        assert not results[0].success
