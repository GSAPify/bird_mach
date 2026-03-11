"""ci_pipeline domain events."""
from dataclasses import dataclass

@dataclass
class CiPipelineCreated:
    id: str
    timestamp: float

@dataclass
class CiPipelineUpdated:
    id: str
    changes: dict
