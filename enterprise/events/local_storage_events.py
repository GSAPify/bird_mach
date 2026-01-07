"""local_storage domain events."""
from dataclasses import dataclass

@dataclass
class LocalStorageCreated:
    id: str
    timestamp: float

@dataclass
class LocalStorageUpdated:
    id: str
    changes: dict
