"""load_testing domain events."""
from dataclasses import dataclass

@dataclass
class LoadTestingCreated:
    id: str
    timestamp: float

@dataclass
class LoadTestingUpdated:
    id: str
    changes: dict
