"""billing domain events."""
from dataclasses import dataclass

@dataclass
class BillingCreated:
    id: str
    timestamp: float

@dataclass
class BillingUpdated:
    id: str
    changes: dict
