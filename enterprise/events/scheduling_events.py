"""scheduling domain events."""
from dataclasses import dataclass

@dataclass
class SchedulingCreated:
    id: str
    timestamp: float

@dataclass
class SchedulingUpdated:
    id: str
    changes: dict
