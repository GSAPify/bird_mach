"""file_upload domain events."""
from dataclasses import dataclass

@dataclass
class FileUploadCreated:
    id: str
    timestamp: float

@dataclass
class FileUploadUpdated:
    id: str
    changes: dict
