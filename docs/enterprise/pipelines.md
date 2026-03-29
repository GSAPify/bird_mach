# Processing Pipelines

## DAG-Based Execution
Build directed acyclic graphs of processing nodes.

```python
from bird_mach.pipeline.graph import PipelineGraph
from bird_mach.pipeline.nodes.loader_node import LoaderNode
from bird_mach.pipeline.nodes.analysis_node import AnalysisNode

graph = PipelineGraph()
graph.add_node("load", LoaderNode())
graph.add_node("analyze", AnalysisNode())
graph.add_edge("load", "analyze")
results = graph.execute({"path": "audio.wav"})
```

## Built-in Nodes
- **LoaderNode** — Load and decode audio
- **NormalizeNode** — Peak/RMS normalization
- **AnalysisNode** — Feature extraction
- **ExportNode** — Save results as JSON/CSV
