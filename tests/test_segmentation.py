"""Tests for bird_mach.segmentation."""

import pytest
import numpy as np

from bird_mach.segmentation import Segment, segment_fixed_length, extract_segment_audio


class TestSegment:
    def test_duration(self):
        s = Segment(start_s=1.0, end_s=3.5)
        assert abs(s.duration_s - 2.5) < 1e-6


class TestFixedLength:
    def test_covers_full_duration(self):
        segs = segment_fixed_length(10.0, segment_length_s=3.0)
        assert segs[0].start_s == 0.0
        assert segs[-1].end_s == 10.0

    def test_overlap(self):
        segs = segment_fixed_length(10.0, segment_length_s=5.0, overlap_s=2.0)
        assert len(segs) > 2
        assert segs[1].start_s < segs[0].end_s

    def test_single_segment(self):
        segs = segment_fixed_length(2.0, segment_length_s=5.0)
        assert len(segs) == 1
        assert segs[0].end_s == 2.0

    def test_zero_segment_length_raises(self):
        # Previously caused an infinite loop; step became 0 and t never advanced.
        with pytest.raises(ValueError, match="segment_length_s must be positive"):
            segment_fixed_length(10.0, segment_length_s=0.0)

    def test_negative_segment_length_raises(self):
        with pytest.raises(ValueError, match="segment_length_s must be positive"):
            segment_fixed_length(10.0, segment_length_s=-1.0)


class TestExtractSegmentAudio:
    """Cover the clamping logic in extract_segment_audio."""

    SR = 1000
    SIGNAL = np.arange(100, dtype=np.float32)  # 0.1 s at 1000 Hz

    def test_normal_extraction(self):
        seg = Segment(start_s=0.01, end_s=0.05)
        out = extract_segment_audio(self.SIGNAL, seg, sr=self.SR)
        assert len(out) == 40

    def test_negative_start_clamped_to_zero(self):
        seg = Segment(start_s=-5.0, end_s=0.05)
        out = extract_segment_audio(self.SIGNAL, seg, sr=self.SR)
        assert out[0] == self.SIGNAL[0]

    def test_end_beyond_signal_clamped(self):
        seg = Segment(start_s=0.09, end_s=999.0)
        out = extract_segment_audio(self.SIGNAL, seg, sr=self.SR)
        assert len(out) == len(self.SIGNAL) - 90

    def test_start_beyond_signal_returns_empty(self):
        seg = Segment(start_s=999.0, end_s=1000.0)
        out = extract_segment_audio(self.SIGNAL, seg, sr=self.SR)
        assert len(out) == 0
