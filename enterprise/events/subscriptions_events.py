"""subscriptions domain events."""
from dataclasses import dataclass

@dataclass
class SubscriptionsCreated:
    id: str
    timestamp: float

@dataclass
class SubscriptionsUpdated:
    id: str
    changes: dict
