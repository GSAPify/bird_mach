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
        self._entries: deque[HistoryEntry] = deque(maxlen=max_entries)

    def record(self, audio_id: str, user_id: str, action: str, **params) -> HistoryEntry:
        entry = HistoryEntry(audio_id=audio_id, user_id=user_id, action=action, params=params)
        self._entries.append(entry)
        return entry

    def get_recent(self, user_id: str, n: int = 20) -> list[HistoryEntry]:
        return [e for e in reversed(self._entries) if e.user_id == user_id][:n]

    def get_for_audio(self, audio_id: str) -> list[HistoryEntry]:
        return [e for e in self._entries if e.audio_id == audio_id]

    @property
    def total(self) -> int:
        return len(self._entries)
