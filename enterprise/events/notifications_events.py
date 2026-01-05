"""notifications domain events."""
from dataclasses import dataclass

@dataclass
class NotificationsCreated:
    id: str
    timestamp: float

@dataclass
class NotificationsUpdated:
    id: str
    changes: dict
