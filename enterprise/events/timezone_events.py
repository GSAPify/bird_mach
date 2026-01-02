"""timezone domain events."""
from dataclasses import dataclass

@dataclass
class TimezoneCreated:
    id: str
    timestamp: float

@dataclass
class TimezoneUpdated:
    id: str
    changes: dict
