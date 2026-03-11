"""pagination domain events."""
from dataclasses import dataclass

@dataclass
class PaginationCreated:
    id: str
    timestamp: float

@dataclass
class PaginationUpdated:
    id: str
    changes: dict
