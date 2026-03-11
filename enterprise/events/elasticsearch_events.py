"""elasticsearch domain events."""
from dataclasses import dataclass

@dataclass
class ElasticsearchCreated:
    id: str
    timestamp: float

@dataclass
class ElasticsearchUpdated:
    id: str
    changes: dict
