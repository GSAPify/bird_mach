"""cd_pipeline domain events."""
from dataclasses import dataclass

@dataclass
class CdPipelineCreated:
    id: str
    timestamp: float

@dataclass
class CdPipelineUpdated:
    id: str
    changes: dict
