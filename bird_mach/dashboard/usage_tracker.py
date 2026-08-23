"""Track API usage and quotas."""
from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timedelta, timezone

class UsageTracker:
    """Track per-user API usage for quota enforcement."""

    def __init__(self, default_quota: int = 1000):
        if default_quota < 1:
            raise ValueError("default_quota must be at least 1")
        self._default_quota = default_quota
        self._usage: dict[str, list[datetime]] = defaultdict(list)
        self._quotas: dict[str, int] = {}

    def record(self, user_id: str) -> None:
        now = datetime.now(timezone.utc)
        calls = self._usage[user_id]
        calls.append(now)
        cutoff = now - timedelta(hours=24)
        self._usage[user_id] = [t for t in calls if t >= cutoff]

    def set_quota(self, user_id: str, quota: int) -> None:
        if quota < 1:
            raise ValueError("quota must be at least 1")
        self._quotas[user_id] = quota

    def get_usage(self, user_id: str, window_hours: int = 24) -> int:
        if window_hours < 1:
            raise ValueError("window_hours must be at least 1")
        cutoff = datetime.now(timezone.utc) - timedelta(hours=window_hours)
        calls = self._usage.get(user_id, [])
        return sum(1 for t in calls if t >= cutoff)

    def check_quota(self, user_id: str) -> tuple[bool, int, int]:
        quota = self._quotas.get(user_id, self._default_quota)
        used = self.get_usage(user_id)
        return used < quota, used, quota

    def get_top_users(self, n: int = 10) -> list[tuple[str, int]]:
        if n < 1:
            raise ValueError("n must be at least 1")
        # Rank by the same 24h window as quota checks, not all-time history.
        counts = [(uid, self.get_usage(uid)) for uid in self._usage]
        counts.sort(key=lambda x: -x[1])
        return counts[:n]
