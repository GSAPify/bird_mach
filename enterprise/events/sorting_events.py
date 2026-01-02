"""sorting domain events."""
from dataclasses import dataclass

@dataclass
class SortingCreated:
    id: str
    timestamp: float

@dataclass
class SortingUpdated:
    id: str
    changes: dict
