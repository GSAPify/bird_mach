"""ab_testing domain events."""
from dataclasses import dataclass

@dataclass
class AbTestingCreated:
    id: str
    timestamp: float

@dataclass
class AbTestingUpdated:
    id: str
    changes: dict
