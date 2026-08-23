"""Real-time presence tracking for collaboration rooms."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta

ONLINE_TTL = timedelta(seconds=60)

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
        allowed = {"status", "cursor_time_s", "is_typing"}
        unknown = set(kwargs) - allowed
        if unknown:
            raise ValueError(f"unsupported presence fields: {sorted(unknown)}")
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
        # A client that disconnects without saying so never updates last_seen,
        # so status alone would keep it online forever.
        cutoff = datetime.now() - ONLINE_TTL
        return [
            p for p in self._users.values()
            if p.status == "online" and p.last_seen >= cutoff
        ]

    @property
    def online_count(self) -> int:
        return len(self.get_online())
