"""blue_green domain events."""
from dataclasses import dataclass

@dataclass
class BlueGreenCreated:
    id: str
    timestamp: float

@dataclass
class BlueGreenUpdated:
    id: str
    changes: dict
