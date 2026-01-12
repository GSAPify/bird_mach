"""health_check domain events."""
from dataclasses import dataclass

@dataclass
class HealthCheckCreated:
    id: str
    timestamp: float

@dataclass
class HealthCheckUpdated:
    id: str
    changes: dict
