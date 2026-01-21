"""real_time domain events."""
from dataclasses import dataclass

@dataclass
class RealTimeCreated:
    id: str
    timestamp: float

@dataclass
class RealTimeUpdated:
    id: str
    changes: dict
