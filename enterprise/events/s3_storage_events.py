"""s3_storage domain events."""
from dataclasses import dataclass

@dataclass
class S3StorageCreated:
    id: str
    timestamp: float

@dataclass
class S3StorageUpdated:
    id: str
    changes: dict
