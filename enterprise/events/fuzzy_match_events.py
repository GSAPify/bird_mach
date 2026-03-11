"""fuzzy_match domain events."""
from dataclasses import dataclass

@dataclass
class FuzzyMatchCreated:
    id: str
    timestamp: float

@dataclass
class FuzzyMatchUpdated:
    id: str
    changes: dict
