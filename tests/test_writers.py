"""Tests for bird_mach.io.writers."""

import numpy as np

from bird_mach.io.writers import save_wav, save_segment


class TestSaveWav:
    def test_creates_file(self, tmp_path):
        y = np.zeros(22050, dtype=np.float32)
        path = save_wav(y, tmp_path / "test.wav", sr=22050)
        assert path.exists()
        assert path.stat().st_size > 0


class TestSaveSegment:
    def test_creates_indexed_file(self, tmp_path):
        y = np.zeros(11025, dtype=np.float32)
        path = save_segment(y, tmp_path / "segs", sr=22050, index=0)
        assert path.name == "segment_0000.wav"
        assert path.exists()

    def test_creates_output_dir(self, tmp_path):
        y = np.zeros(11025, dtype=np.float32)
        out = tmp_path / "new_dir"
        save_segment(y, out, sr=22050, index=1)
        assert out.is_dir()
