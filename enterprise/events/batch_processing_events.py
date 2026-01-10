"""batch_processing domain events."""
from dataclasses import dataclass

@dataclass
class BatchProcessingCreated:
    id: str
    timestamp: float

@dataclass
class BatchProcessingUpdated:
    id: str
    changes: dict
