"""signing domain events."""
from dataclasses import dataclass

@dataclass
class SigningCreated:
    id: str
    timestamp: float

@dataclass
class SigningUpdated:
    id: str
    changes: dict
