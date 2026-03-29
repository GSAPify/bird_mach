"""Pipeline node abstraction."""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from typing import Protocol

class PipelineNode(Protocol):
    name: str
    def process(self, data: dict) -> dict: ...

@dataclass
class NodeResult:
    node_name: str
    success: bool
    output: dict
    duration_ms: float = 0.0
    error: str | None = None
