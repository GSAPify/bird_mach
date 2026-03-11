"""unit_testing domain events."""
from dataclasses import dataclass

@dataclass
class UnitTestingCreated:
    id: str
    timestamp: float

@dataclass
class UnitTestingUpdated:
    id: str
    changes: dict
