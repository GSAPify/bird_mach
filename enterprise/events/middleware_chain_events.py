"""middleware_chain domain events."""
from dataclasses import dataclass

@dataclass
class MiddlewareChainCreated:
    id: str
    timestamp: float

@dataclass
class MiddlewareChainUpdated:
    id: str
    changes: dict
