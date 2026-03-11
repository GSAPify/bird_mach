"""runbooks domain events."""
from dataclasses import dataclass

@dataclass
class RunbooksCreated:
    id: str
    timestamp: float

@dataclass
class RunbooksUpdated:
    id: str
    changes: dict
