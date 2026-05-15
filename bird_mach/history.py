"""Analysis history tracking."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque

@dataclass
class HistoryEntry:
    audio_id: str
    user_id: str
    action: str
    params: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

class HistoryTracker:
    def __init__(self, max_entries: int = 500):
        if max_entries < 1:
            raise ValueError("max_entries must be at least 1")
        self._entries: deque[HistoryEntry] = deque(maxlen=max_entries)

    def record(self, audio_id: str, user_id: str, action: str, **params) -> HistoryEntry:
        if not audio_id or not audio_id.strip():
            raise ValueError("audio_id must not be empty")
        if not user_id or not user_id.strip():
            raise ValueError("user_id must not be empty")
        if not action or not action.strip():
            raise ValueError("action must not be empty")
        entry = HistoryEntry(audio_id=audio_id, user_id=user_id, action=action, params=params)
        self._entries.append(entry)
        return entry

    def get_recent(self, user_id: str, n: int = 20) -> list[HistoryEntry]:
        if n < 1:
            raise ValueError("n must be at least 1")
        return [e for e in reversed(self._entries) if e.user_id == user_id][:n]

    def get_for_audio(self, audio_id: str) -> list[HistoryEntry]:
        """Entries for one audio id, newest first (matching get_recent)."""
        return [e for e in reversed(self._entries) if e.audio_id == audio_id]

    @property
    def total(self) -> int:
        return len(self._entries)
