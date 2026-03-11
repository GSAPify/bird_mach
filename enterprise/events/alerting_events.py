"""alerting domain events."""
from dataclasses import dataclass

@dataclass
class AlertingCreated:
    id: str
    timestamp: float

@dataclass
class AlertingUpdated:
    id: str
    changes: dict
