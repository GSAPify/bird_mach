"""key_rotation domain events."""
from dataclasses import dataclass

@dataclass
class KeyRotationCreated:
    id: str
    timestamp: float

@dataclass
class KeyRotationUpdated:
    id: str
    changes: dict
