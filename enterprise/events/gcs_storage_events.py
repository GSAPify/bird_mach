"""gcs_storage domain events."""
from dataclasses import dataclass

@dataclass
class GcsStorageCreated:
    id: str
    timestamp: float

@dataclass
class GcsStorageUpdated:
    id: str
    changes: dict
