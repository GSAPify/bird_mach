"""azure_blob domain events."""
from dataclasses import dataclass

@dataclass
class AzureBlobCreated:
    id: str
    timestamp: float

@dataclass
class AzureBlobUpdated:
    id: str
    changes: dict
