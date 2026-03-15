"""Usage leaderboard for gamification."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class LeaderboardEntry:
    user_id: str
    display_name: str
    score: int
    rank: int

class Leaderboard:
    def __init__(self):
        self._scores: dict[str, tuple[str, int]] = {}

    def add_points(self, user_id: str, name: str, points: int) -> None:
        current = self._scores.get(user_id, (name, 0))
        self._scores[user_id] = (name, current[1] + points)

    def get_top(self, n: int = 10) -> list[LeaderboardEntry]:
        sorted_users = sorted(self._scores.items(), key=lambda x: -x[1][1])
        return [
            LeaderboardEntry(uid, name, score, rank+1)
            for rank, (uid, (name, score)) in enumerate(sorted_users[:n])
        ]

    def get_rank(self, user_id: str) -> int | None:
        for entry in self.get_top(len(self._scores)):
            if entry.user_id == user_id:
                return entry.rank
        return None
