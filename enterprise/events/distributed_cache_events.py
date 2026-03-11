"""distributed_cache domain events."""
from dataclasses import dataclass

@dataclass
class DistributedCacheCreated:
    id: str
    timestamp: float

@dataclass
class DistributedCacheUpdated:
    id: str
    changes: dict
