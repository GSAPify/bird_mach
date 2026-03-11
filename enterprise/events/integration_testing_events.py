"""integration_testing domain events."""
from dataclasses import dataclass

@dataclass
class IntegrationTestingCreated:
    id: str
    timestamp: float

@dataclass
class IntegrationTestingUpdated:
    id: str
    changes: dict
