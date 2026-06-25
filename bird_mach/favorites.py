"""Favorites and bookmarks for audio files."""
from __future__ import annotations
from collections import defaultdict
from datetime import datetime

class FavoritesManager:
    def __init__(self):
        self._favorites: dict[str, dict[str, datetime]] = defaultdict(dict)

    def add(self, user_id: str, audio_id: str) -> None:
        if not user_id or not user_id.strip():
            raise ValueError("user_id must not be empty")
        if not audio_id or not audio_id.strip():
            raise ValueError("audio_id must not be empty")
        self._favorites[user_id][audio_id] = datetime.now()

    def remove(self, user_id: str, audio_id: str) -> None:
        if user_id in self._favorites:
            self._favorites[user_id].pop(audio_id, None)

    def get(self, user_id: str) -> list[str]:
        stamps = self._favorites.get(user_id, {})
        return sorted(stamps, key=lambda k: stamps[k], reverse=True)

    def is_favorite(self, user_id: str, audio_id: str) -> bool:
        return audio_id in self._favorites.get(user_id, {})

    def count(self, user_id: str) -> int:
        return len(self._favorites.get(user_id, {}))
