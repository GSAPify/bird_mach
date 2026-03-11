"""tracing domain events."""
from dataclasses import dataclass

@dataclass
class TracingCreated:
    id: str
    timestamp: float

@dataclass
class TracingUpdated:
    id: str
    changes: dict
