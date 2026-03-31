"""Tests for error tracker."""
from bird_mach.observability.error_tracker import ErrorTracker

class TestErrorTracker:
    def test_track(self):
        et = ErrorTracker()
        et.track(ValueError("bad input"))
        assert et.total_errors == 1
        assert et.unique_errors == 1

    def test_dedup(self):
        et = ErrorTracker()
        et.track(ValueError("same"))
        et.track(ValueError("same"))
        assert et.total_errors == 2
        assert et.unique_errors == 1

    def test_top_errors(self):
        et = ErrorTracker()
        for _ in range(5):
            et.track(ValueError("common"))
        et.track(TypeError("rare"))
        top = et.top_errors(2)
        assert top[0].type == "ValueError"
        assert top[0].count == 5
