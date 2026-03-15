"""Activity feed for tracking user actions."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque

@dataclass
class Activity:
    user_id: str
    action: str
    resource_type: str
    resource_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

class ActivityFeed:
    def __init__(self, max_items: int = 1000):
        self._items: deque[Activity] = deque(maxlen=max_items)

    def log(self, user_id: str, action: str,
            resource_type: str, resource_id: str, **metadata) -> Activity:
        activity = Activity(
            user_id=user_id, action=action,
            resource_type=resource_type, resource_id=resource_id,
            metadata=metadata,
        )
        self._items.append(activity)
        return activity

    def get_recent(self, n: int = 20) -> list[Activity]:
        items = list(self._items)
        items.reverse()
        return items[:n]

    def get_for_user(self, user_id: str, n: int = 20) -> list[Activity]:
        return [a for a in reversed(self._items) if a.user_id == user_id][:n]

    def get_for_resource(self, resource_type: str, resource_id: str) -> list[Activity]:
        return [a for a in self._items
                if a.resource_type == resource_type and a.resource_id == resource_id]

    @property
    def total_activities(self) -> int:
        return len(self._items)
