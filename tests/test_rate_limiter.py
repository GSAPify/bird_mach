"""Tests for rate limiter."""
from bird_mach.rate_limiter import TokenBucketLimiter
class TestTokenBucket:
    def test_allows_within_capacity(self):
        rl = TokenBucketLimiter(capacity=10)
        result = rl.check("user1")
        assert result.allowed
        assert result.remaining == 9
    def test_exhaustion(self):
        rl = TokenBucketLimiter(capacity=2, refill_rate=0.001)
        rl.check("u1")
        rl.check("u1")
        result = rl.check("u1")
        assert not result.allowed
