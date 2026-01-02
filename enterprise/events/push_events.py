"""push domain events."""
from dataclasses import dataclass

@dataclass
class PushCreated:
    id: str
    timestamp: float

@dataclass
class PushUpdated:
    id: str
    changes: dict
