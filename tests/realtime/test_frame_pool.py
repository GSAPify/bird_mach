"""Tests for frame pool."""
import numpy as np
from bird_mach.realtime.frame_pool import FramePool

class TestFramePool:
    def test_acquire(self):
        pool = FramePool(frame_size=1024, pool_size=5)
        frame = pool.acquire()
        assert len(frame) == 1024

    def test_release_and_reuse(self):
        pool = FramePool(frame_size=1024, pool_size=5)
        f = pool.acquire()
        pool.release(f)
        f2 = pool.acquire()
        assert np.allclose(f2, 0)

    def test_stats(self):
        pool = FramePool(frame_size=512, pool_size=2)
        pool.acquire()
        assert pool.stats["reused"] == 1


def test_release_ignores_wrong_dtype():
    import numpy as np
    from bird_mach.realtime.frame_pool import FramePool
    pool = FramePool(frame_size=8, pool_size=2)
    pool.acquire()
    pool.release(np.zeros(8, dtype=np.float64))
    assert pool.stats["pool_size"] == 1
    assert pool.acquire().dtype == np.float32


def test_double_release_does_not_share_buffers():
    from bird_mach.realtime.frame_pool import FramePool
    pool = FramePool(frame_size=8, pool_size=4)
    while pool.stats["pool_size"]:
        pool.acquire()
    frame = pool.acquire()
    pool.release(frame)
    pool.release(frame)
    assert pool.acquire() is not pool.acquire()
