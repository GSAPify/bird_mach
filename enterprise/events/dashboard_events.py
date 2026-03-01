"""dashboard domain events."""
from dataclasses import dataclass

@dataclass
class DashboardCreated:
    id: str
    timestamp: float

@dataclass
class DashboardUpdated:
    id: str
    changes: dict
