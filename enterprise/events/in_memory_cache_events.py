"""in_memory_cache domain events."""
from dataclasses import dataclass

@dataclass
class InMemoryCacheCreated:
    id: str
    timestamp: float

@dataclass
class InMemoryCacheUpdated:
    id: str
    changes: dict
