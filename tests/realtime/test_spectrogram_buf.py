"""Tests for spectrogram buffer."""
import numpy as np
from bird_mach.realtime.spectrogram_buffer import SpectrogramBuffer
class TestSpectrogramBuffer:
    def test_push(self):
        buf = SpectrogramBuffer(n_frames=10, n_bins=32)
        buf.push(np.zeros(32))
        assert buf.frame_count == 1
    def test_get_image(self):
        buf = SpectrogramBuffer(n_frames=5, n_bins=16)
        for _ in range(3):
            buf.push(np.random.randn(16).astype(np.float32))
        img = buf.get_image()
        assert img.shape == (16, 3)


def test_get_image_does_not_expose_internal_buffer():
    import numpy as np
    from bird_mach.realtime.spectrogram_buffer import SpectrogramBuffer
    buf = SpectrogramBuffer(n_frames=4, n_bins=2)
    buf.push(np.array([1.0, 2.0]))
    buf.get_image()[:] = 99
    assert buf.get_image()[:, 0].tolist() == [1.0, 2.0]
