"""api_docs domain events."""
from dataclasses import dataclass

@dataclass
class ApiDocsCreated:
    id: str
    timestamp: float

@dataclass
class ApiDocsUpdated:
    id: str
    changes: dict
