"""Tests for bird_mach.segmentation."""

from bird_mach.segmentation import Segment, segment_fixed_length


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
