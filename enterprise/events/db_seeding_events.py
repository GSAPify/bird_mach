"""db_seeding domain events."""
from dataclasses import dataclass

@dataclass
class DbSeedingCreated:
    id: str
    timestamp: float

@dataclass
class DbSeedingUpdated:
    id: str
    changes: dict
