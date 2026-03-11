"""metrics domain events."""
from dataclasses import dataclass

@dataclass
class MetricsCreated:
    id: str
    timestamp: float

@dataclass
class MetricsUpdated:
    id: str
    changes: dict
