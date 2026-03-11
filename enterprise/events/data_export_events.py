"""data_export domain events."""
from dataclasses import dataclass

@dataclass
class DataExportCreated:
    id: str
    timestamp: float

@dataclass
class DataExportUpdated:
    id: str
    changes: dict
