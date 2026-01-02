"""jwt_auth domain events."""
from dataclasses import dataclass

@dataclass
class JwtAuthCreated:
    id: str
    timestamp: float

@dataclass
class JwtAuthUpdated:
    id: str
    changes: dict
