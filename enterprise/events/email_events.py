"""email domain events."""
from dataclasses import dataclass

@dataclass
class EmailCreated:
    id: str
    timestamp: float

@dataclass
class EmailUpdated:
    id: str
    changes: dict
