"""redis_cache domain events."""
from dataclasses import dataclass

@dataclass
class RedisCacheCreated:
    id: str
    timestamp: float

@dataclass
class RedisCacheUpdated:
    id: str
    changes: dict
