"""Tests for loudness meter."""
import numpy as np
from bird_mach.realtime.loudness import LoudnessMeter
class TestLoudnessMeter:
    def test_silence(self):
        meter = LoudnessMeter()
        result = meter.process(np.zeros(1024))
        assert result["momentary_lufs"] < -60
    def test_signal(self):
        meter = LoudnessMeter()
        result = meter.process(np.ones(1024)*0.5)
        assert result["momentary_lufs"] > -20


def test_empty_input_before_any_audio_reports_floor():
    import numpy as np
    from bird_mach.realtime.loudness import LoudnessMeter
    assert LoudnessMeter().process(np.array([]))["integrated_lufs"] == -70.0
