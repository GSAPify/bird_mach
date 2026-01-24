"""api_keys domain events."""
from dataclasses import dataclass

@dataclass
class ApiKeysCreated:
    id: str
    timestamp: float

@dataclass
class ApiKeysUpdated:
    id: str
    changes: dict
