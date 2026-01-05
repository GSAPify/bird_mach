"""search domain events."""
from dataclasses import dataclass

@dataclass
class SearchCreated:
    id: str
    timestamp: float

@dataclass
class SearchUpdated:
    id: str
    changes: dict
