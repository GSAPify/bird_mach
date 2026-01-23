"""e2e_testing domain events."""
from dataclasses import dataclass

@dataclass
class E2ETestingCreated:
    id: str
    timestamp: float

@dataclass
class E2ETestingUpdated:
    id: str
    changes: dict
