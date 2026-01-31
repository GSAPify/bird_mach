"""full_text_search domain events."""
from dataclasses import dataclass

@dataclass
class FullTextSearchCreated:
    id: str
    timestamp: float

@dataclass
class FullTextSearchUpdated:
    id: str
    changes: dict
