"""Immutable audit log for security-sensitive operations."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from collections import deque

@dataclass(frozen=True)
class AuditEntry:
    timestamp: datetime
    user_id: str
    action: str
    resource: str
    ip_address: str = ""
    details: str = ""

class AuditLog:
    def __init__(self, max_entries: int = 10000):
        if max_entries < 1:
            raise ValueError("max_entries must be at least 1")
        self._log: deque[AuditEntry] = deque(maxlen=max_entries)

    def record(self, user_id: str, action: str, resource: str,
               ip: str = "", details: str = "") -> AuditEntry:
        entry = AuditEntry(
            timestamp=datetime.now(timezone.utc), user_id=user_id,
            action=action, resource=resource,
            ip_address=ip, details=details,
        )
        self._log.append(entry)
        return entry

    def query(self, user_id: str | None = None, action: str | None = None,
              limit: int = 50) -> list[AuditEntry]:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        results = list(self._log)
        if user_id is not None:
            results = [e for e in results if e.user_id == user_id]
        if action is not None:
            results = [e for e in results if e.action == action]
        return list(reversed(results))[:limit]

    @property
    def total_entries(self) -> int:
        return len(self._log)
