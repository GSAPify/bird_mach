"""analytics domain events."""
from dataclasses import dataclass

@dataclass
class AnalyticsCreated:
    id: str
    timestamp: float

@dataclass
class AnalyticsUpdated:
    id: str
    changes: dict
