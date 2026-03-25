"""Tests for batch progress."""
from bird_mach.batch.progress import BatchProgress

class TestBatchProgress:
    def test_percent(self):
        p = BatchProgress(total=10, completed=5)
        assert p.percent == 50.0

    def test_remaining(self):
        p = BatchProgress(total=10, completed=3, failed=2)
        assert p.remaining == 5

    def test_tick(self):
        p = BatchProgress(total=5)
        p.tick_success()
        p.tick_failure()
        assert p.completed == 1
        assert p.failed == 1

    def test_all_done(self):
        p = BatchProgress(total=2, completed=2)
        assert p.percent == 100.0
