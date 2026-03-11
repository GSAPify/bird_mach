"""event_bus domain events."""
from dataclasses import dataclass

@dataclass
class EventBusCreated:
    id: str
    timestamp: float

@dataclass
class EventBusUpdated:
    id: str
    changes: dict
