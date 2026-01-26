"""db_migration domain events."""
from dataclasses import dataclass

@dataclass
class DbMigrationCreated:
    id: str
    timestamp: float

@dataclass
class DbMigrationUpdated:
    id: str
    changes: dict
