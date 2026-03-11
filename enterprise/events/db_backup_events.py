"""db_backup domain events."""
from dataclasses import dataclass

@dataclass
class DbBackupCreated:
    id: str
    timestamp: float

@dataclass
class DbBackupUpdated:
    id: str
    changes: dict
