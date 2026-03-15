"""Tests for leaderboard."""
from bird_mach.dashboard.leaderboard import Leaderboard
class TestLeaderboard:
    def test_add_and_rank(self):
        lb = Leaderboard()
        lb.add_points("u1", "Alice", 100)
        lb.add_points("u2", "Bob", 200)
        top = lb.get_top()
        assert top[0].display_name == "Bob"
    def test_get_rank(self):
        lb = Leaderboard()
        lb.add_points("u1", "A", 50)
        lb.add_points("u2", "B", 100)
        assert lb.get_rank("u2") == 1
