"""Real-time presence tracking for collaboration rooms."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class UserPresence:
    user_id: str
    status: str = "online"
    last_seen: datetime = field(default_factory=datetime.now)
    cursor_time_s: float = 0.0
    is_typing: bool = False

class PresenceTracker:
    def __init__(self):
        self._users: dict[str, UserPresence] = {}

    def update(self, user_id: str, **kwargs) -> UserPresence:
        if user_id not in self._users:
            self._users[user_id] = UserPresence(user_id=user_id)
        p = self._users[user_id]
        p.last_seen = datetime.now()
        for k, v in kwargs.items():
            setattr(p, k, v)
        return p

    def remove(self, user_id: str) -> None:
        self._users.pop(user_id, None)

    def get_online(self) -> list[UserPresence]:
        return [p for p in self._users.values() if p.status == "online"]

    @property
    def online_count(self) -> int:
        return len(self.get_online())
