"""vector_search domain events."""
from dataclasses import dataclass

@dataclass
class VectorSearchCreated:
    id: str
    timestamp: float

@dataclass
class VectorSearchUpdated:
    id: str
    changes: dict
