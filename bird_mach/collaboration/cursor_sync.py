"""Cursor synchronization for collaborative audio review."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class CursorState:
    user_id: str
    position_s: float
    is_playing: bool = False
    color: str = "#38bdf8"

class CursorSyncManager:
    """Sync playback cursors across collaborators."""
    def __init__(self):
        self._cursors: dict[str, CursorState] = {}

    def update(self, user_id: str, position_s: float, is_playing: bool = False) -> CursorState:
        cursor = CursorState(user_id=user_id, position_s=position_s, is_playing=is_playing)
        self._cursors[user_id] = cursor
        return cursor

    def get_all(self) -> list[CursorState]:
        return list(self._cursors.values())

    def remove(self, user_id: str) -> None:
        self._cursors.pop(user_id, None)
