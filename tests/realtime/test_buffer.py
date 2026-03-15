"""Tests for ring buffer."""
import numpy as np
from bird_mach.realtime.buffer import RingBuffer

class TestRingBuffer:
    def test_write_and_read(self):
        buf = RingBuffer(100)
        buf.write(np.ones(50, dtype=np.float32))
        assert buf.count == 50
        data = buf.read()
        assert len(data) == 50
        assert np.allclose(data, 1.0)

    def test_overflow_wraps(self):
        buf = RingBuffer(10)
        buf.write(np.arange(15, dtype=np.float32))
        assert buf.count == 10
        data = buf.read()
        assert data[-1] == 14.0

    def test_clear(self):
        buf = RingBuffer(50)
        buf.write(np.ones(30, dtype=np.float32))
        buf.clear()
        assert buf.count == 0

    def test_is_full(self):
        buf = RingBuffer(10)
        assert not buf.is_full
        buf.write(np.ones(10, dtype=np.float32))
        assert buf.is_full

    def test_read_partial(self):
        buf = RingBuffer(100)
        buf.write(np.arange(50, dtype=np.float32))
        data = buf.read(10)
        assert len(data) == 10
