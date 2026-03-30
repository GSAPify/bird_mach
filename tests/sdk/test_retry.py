"""Tests for SDK retry logic."""
from bird_mach.sdk.retry import RetryConfig, with_retry

class TestRetryConfig:
    def test_delay_increases(self):
        cfg = RetryConfig(jitter=False)
        assert cfg.delay_for(0) == 0.5
        assert cfg.delay_for(1) == 1.0
        assert cfg.delay_for(2) == 2.0

    def test_max_delay(self):
        cfg = RetryConfig(base_delay=10, jitter=False)
        assert cfg.delay_for(10) == 30.0

class TestWithRetry:
    def test_succeeds(self):
        assert with_retry(lambda: 42) == 42

    def test_retries_then_succeeds(self):
        attempts = [0]
        def flaky():
            attempts[0] += 1
            if attempts[0] < 3:
                raise ValueError("fail")
            return "ok"
        result = with_retry(flaky, RetryConfig(max_retries=3, base_delay=0.001))
        assert result == "ok"
