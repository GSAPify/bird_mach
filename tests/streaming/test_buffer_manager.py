"""Tests for adaptive buffer."""
from bird_mach.streaming.buffer_manager import AdaptiveBuffer

class TestAdaptiveBuffer:
    def test_push_pull(self):
        buf = AdaptiveBuffer()
        buf.push(b"hello")
        data = buf.pull(5)
        assert data == b"hello"

    def test_overflow(self):
        buf = AdaptiveBuffer(max_size=10)
        assert not buf.push(b"x" * 20)
        assert buf.stats["overflows"] == 1

    def test_adapt_high_latency(self):
        buf = AdaptiveBuffer(min_size=100, max_size=10000)
        old = buf._current_size
        buf.adapt(300.0)
        assert buf._current_size > old
