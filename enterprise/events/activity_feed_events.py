"""activity_feed domain events."""
from dataclasses import dataclass

@dataclass
class ActivityFeedCreated:
    id: str
    timestamp: float

@dataclass
class ActivityFeedUpdated:
    id: str
    changes: dict
