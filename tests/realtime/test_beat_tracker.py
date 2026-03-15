"""Tests for beat tracker."""
import numpy as np
from bird_mach.realtime.beat_tracker import RealtimeBeatTracker
class TestBeatTracker:
    def test_init(self):
        bt = RealtimeBeatTracker()
        assert bt.beat_count == 0
        assert bt.bpm == 0.0
    def test_process(self):
        bt = RealtimeBeatTracker()
        for i in range(20):
            bt.process(np.random.randn(100), float(i)*0.5)
