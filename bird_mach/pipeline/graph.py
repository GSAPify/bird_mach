"""Directed acyclic graph for pipeline execution."""
from __future__ import annotations
import time
from bird_mach.pipeline.node import NodeResult

class PipelineGraph:
    """Execute pipeline nodes in topological order."""
    def __init__(self):
        self._nodes: dict[str, object] = {}
        self._edges: dict[str, list[str]] = {}

    def add_node(self, name: str, node) -> None:
        self._nodes[name] = node
        self._edges.setdefault(name, [])

    def add_edge(self, from_node: str, to_node: str) -> None:
        self._edges.setdefault(from_node, []).append(to_node)

    def _topo_sort(self) -> list[str]:
        visited = set()
        in_progress = set()
        order = []
        def dfs(n):
            if n in visited:
                return
            if n in in_progress:
                raise ValueError(f"cycle detected at node {n!r}")
            in_progress.add(n)
            for dep in self._edges.get(n, []):
                dfs(dep)
            in_progress.discard(n)
            visited.add(n)
            order.append(n)
        for n in self._nodes:
            dfs(n)
        return list(reversed(order))

    def execute(self, initial_data: dict) -> list[NodeResult]:
        results = []
        data = dict(initial_data)
        for name in self._topo_sort():
            node = self._nodes[name]
            start = time.time()
            try:
                output = node.process(data)
                data.update(output)
                dur = (time.time() - start) * 1000
                results.append(NodeResult(name, True, output, dur))
            except Exception as e:
                dur = (time.time() - start) * 1000
                results.append(NodeResult(name, False, {}, dur, str(e)))
        return results

    @property
    def node_count(self) -> int:
        return len(self._nodes)
