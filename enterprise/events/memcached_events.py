"""memcached domain events."""
from dataclasses import dataclass

@dataclass
class MemcachedCreated:
    id: str
    timestamp: float

@dataclass
class MemcachedUpdated:
    id: str
    changes: dict
