"""Tests for recorder."""
import numpy as np
from bird_mach.realtime.recorder import SessionRecorder
class TestRecorder:
    def test_start_stop(self):
        r = SessionRecorder(max_duration_s=1.0, sr=22050)
        r.start()
        r.add_chunk(np.zeros(11025, dtype=np.float32))
        data = r.stop()
        assert len(data) == 11025
    def test_max_duration(self):
        r = SessionRecorder(max_duration_s=0.5, sr=22050)
        r.start()
        assert r.add_chunk(np.zeros(11025, dtype=np.float32))
        assert not r.add_chunk(np.zeros(11025, dtype=np.float32))
