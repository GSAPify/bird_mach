"""Tests for retry policy."""
from bird_mach.webhooks.retry import RetryPolicy, RetryQueue

class TestRetryPolicy:
    def test_delay_increases(self):
        p = RetryPolicy(base_delay_s=1.0, backoff_factor=2.0)
        assert p.get_delay(0) == 1.0
        assert p.get_delay(1) == 2.0
        assert p.get_delay(2) == 4.0

    def test_max_delay(self):
        p = RetryPolicy(base_delay_s=1.0, max_delay_s=10.0, backoff_factor=100)
        assert p.get_delay(5) == 10.0

    def test_should_retry(self):
        p = RetryPolicy(max_retries=3)
        assert p.should_retry(2)
        assert not p.should_retry(3)

class TestRetryQueue:
    def test_enqueue(self):
        q = RetryQueue()
        q.enqueue({"url": "test"}, attempt=0)
        assert q.pending_count == 1
