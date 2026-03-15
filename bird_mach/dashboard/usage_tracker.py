"""Track API usage and quotas."""
from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timedelta

class UsageTracker:
    """Track per-user API usage for quota enforcement."""

    def __init__(self, default_quota: int = 1000):
        self._default_quota = default_quota
        self._usage: dict[str, list[datetime]] = defaultdict(list)
        self._quotas: dict[str, int] = {}

    def record(self, user_id: str) -> None:
        self._usage[user_id].append(datetime.now())

    def set_quota(self, user_id: str, quota: int) -> None:
        self._quotas[user_id] = quota

    def get_usage(self, user_id: str, window_hours: int = 24) -> int:
        cutoff = datetime.now() - timedelta(hours=window_hours)
        calls = self._usage.get(user_id, [])
        return sum(1 for t in calls if t >= cutoff)

    def check_quota(self, user_id: str) -> tuple[bool, int, int]:
        quota = self._quotas.get(user_id, self._default_quota)
        used = self.get_usage(user_id)
        return used < quota, used, quota

    def get_top_users(self, n: int = 10) -> list[tuple[str, int]]:
        counts = [(uid, len(calls)) for uid, calls in self._usage.items()]
        counts.sort(key=lambda x: -x[1])
        return counts[:n]
