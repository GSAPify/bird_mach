"""connection_pool domain events."""
from dataclasses import dataclass

@dataclass
class ConnectionPoolCreated:
    id: str
    timestamp: float

@dataclass
class ConnectionPoolUpdated:
    id: str
    changes: dict
