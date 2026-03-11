"""filtering domain events."""
from dataclasses import dataclass

@dataclass
class FilteringCreated:
    id: str
    timestamp: float

@dataclass
class FilteringUpdated:
    id: str
    changes: dict
