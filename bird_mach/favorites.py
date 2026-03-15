"""Favorites and bookmarks for audio files."""
from __future__ import annotations
from collections import defaultdict
from datetime import datetime

class FavoritesManager:
    def __init__(self):
        self._favorites: dict[str, dict[str, datetime]] = defaultdict(dict)

    def add(self, user_id: str, audio_id: str) -> None:
        self._favorites[user_id][audio_id] = datetime.now()

    def remove(self, user_id: str, audio_id: str) -> None:
        self._favorites[user_id].pop(audio_id, None)

    def get(self, user_id: str) -> list[str]:
        return sorted(self._favorites[user_id].keys(),
                      key=lambda k: self._favorites[user_id][k], reverse=True)

    def is_favorite(self, user_id: str, audio_id: str) -> bool:
        return audio_id in self._favorites.get(user_id, {})

    def count(self, user_id: str) -> int:
        return len(self._favorites.get(user_id, {}))
