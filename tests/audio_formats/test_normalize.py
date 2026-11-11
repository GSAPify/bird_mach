"""Tests for normalization."""
import numpy as np
from bird_mach.audio_formats.normalize import peak_normalize, rms_normalize, dc_remove

class TestNormalize:
    def test_peak(self):
        y = np.array([0.5, -0.3, 0.8], dtype=np.float32)
        result = peak_normalize(y, target_db=-1.0)
        assert np.max(np.abs(result)) < 1.01

    def test_rms(self):
        y = np.random.randn(1000).astype(np.float32) * 0.1
        result = rms_normalize(y, target_db=-20.0)
        rms = np.sqrt(np.mean(result ** 2))
        assert abs(20 * np.log10(rms) - (-20.0)) < 1.0

    def test_dc_remove(self):
        y = np.ones(100, dtype=np.float32) * 0.5
        result = dc_remove(y)
        assert abs(np.mean(result)) < 1e-6

    def test_silence(self):
        y = np.zeros(100, dtype=np.float32)
        assert np.allclose(peak_normalize(y), y)


def test_peak_normalize_with_nan_returns_input():
    import numpy as np
    from bird_mach.audio_formats.normalize import peak_normalize
    y = np.array([0.5, np.nan, 0.2])
    out = peak_normalize(y)
    assert out[0] == 0.5 and out[2] == 0.2


def test_rms_normalize_int16_input():
    import numpy as np
    from bird_mach.audio_formats.normalize import rms_normalize
    out = rms_normalize(np.full(1000, 20000, dtype=np.int16), target_db=-20.0)
    assert np.allclose(out, 0.1)
