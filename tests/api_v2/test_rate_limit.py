"""Tests for rate limiter."""
from bird_mach.api.v2.rate_limit import SlidingWindowLimiter

class TestSlidingWindowLimiter:
    def test_allows(self):
        rl = SlidingWindowLimiter(max_requests=10)
        result = rl.check("user1")
        assert result.allowed
        assert result.remaining == 9

    def test_blocks_when_full(self):
        rl = SlidingWindowLimiter(max_requests=2, window_s=60)
        rl.check("u1")
        rl.check("u1")
        result = rl.check("u1")
        assert not result.allowed
        assert result.retry_after_s > 0
