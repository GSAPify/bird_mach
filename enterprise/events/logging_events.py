"""logging domain events."""
from dataclasses import dataclass

@dataclass
class LoggingCreated:
    id: str
    timestamp: float

@dataclass
class LoggingUpdated:
    id: str
    changes: dict
