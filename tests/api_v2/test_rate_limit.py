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


def test_idle_keys_are_swept(monkeypatch):
    from bird_mach.api.v2.rate_limit import SlidingWindowLimiter
    clock = [1000.0]
    monkeypatch.setattr("bird_mach.api.v2.rate_limit.time.time", lambda: clock[0])
    rl = SlidingWindowLimiter(window_s=10.0, max_requests=5)
    for i in range(1024):
        rl.check(f"ip-{i}")
    clock[0] += 60  # every key's window has expired
    rl.check("fresh")
    assert set(rl._requests) == {"fresh"}
