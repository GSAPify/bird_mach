"""caching domain events."""
from dataclasses import dataclass

@dataclass
class CachingCreated:
    id: str
    timestamp: float

@dataclass
class CachingUpdated:
    id: str
    changes: dict
