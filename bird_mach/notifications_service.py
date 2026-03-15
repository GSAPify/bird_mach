"""Notification dispatch service for Mach."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
from enum import Enum

class NotificationType(Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"

@dataclass
class Notification:
    id: str
    user_id: str
    type: NotificationType
    title: str
    message: str
    created_at: datetime = field(default_factory=datetime.now)
    read: bool = False
    action_url: str | None = None

class NotificationService:
    def __init__(self, max_per_user: int = 100):
        self._notifications: dict[str, deque[Notification]] = {}
        self._max = max_per_user
        self._counter = 0

    def send(self, user_id: str, type: NotificationType,
             title: str, message: str, action_url: str | None = None) -> Notification:
        self._counter += 1
        notif = Notification(
            id=f"n-{self._counter}", user_id=user_id,
            type=type, title=title, message=message, action_url=action_url,
        )
        if user_id not in self._notifications:
            self._notifications[user_id] = deque(maxlen=self._max)
        self._notifications[user_id].append(notif)
        return notif

    def get_unread(self, user_id: str) -> list[Notification]:
        return [n for n in self._notifications.get(user_id, []) if not n.read]

    def mark_read(self, user_id: str, notification_id: str) -> bool:
        for n in self._notifications.get(user_id, []):
            if n.id == notification_id:
                n.read = True
                return True
        return False

    def mark_all_read(self, user_id: str) -> int:
        count = 0
        for n in self._notifications.get(user_id, []):
            if not n.read:
                n.read = True
                count += 1
        return count

    def unread_count(self, user_id: str) -> int:
        return len(self.get_unread(user_id))
