"""rbac domain events."""
from dataclasses import dataclass

@dataclass
class RbacCreated:
    id: str
    timestamp: float

@dataclass
class RbacUpdated:
    id: str
    changes: dict
