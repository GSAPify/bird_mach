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
    def test_denied_reset_at_accounts_for_partial_token(self, monkeypatch):
        clock = [1000.0]
        monkeypatch.setattr("bird_mach.rate_limiter.time.time", lambda: clock[0])
        rl = TokenBucketLimiter(capacity=1, refill_rate=1.0)
        rl.check("u1")
        clock[0] += 0.75  # 0.75 tokens refilled; 0.25s until the next one
        result = rl.check("u1")
        assert not result.allowed
        assert abs(result.reset_at - (clock[0] + 0.25)) < 1e-9
