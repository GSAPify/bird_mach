"""adrs domain events."""
from dataclasses import dataclass

@dataclass
class AdrsCreated:
    id: str
    timestamp: float

@dataclass
class AdrsUpdated:
    id: str
    changes: dict
