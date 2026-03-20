"""Tests for HLS generator."""
import numpy as np
from bird_mach.streaming.hls import HLSGenerator

class TestHLSGenerator:
    def test_segment(self):
        gen = HLSGenerator(segment_duration_s=1.0, sr=22050)
        audio = np.zeros(44100, dtype=np.float32)
        segments = gen.segment(audio)
        assert len(segments) == 2

    def test_playlist(self):
        gen = HLSGenerator(segment_duration_s=1.0, sr=22050)
        audio = np.zeros(22050, dtype=np.float32)
        segs = gen.segment(audio)
        playlist = gen.generate_playlist(segs)
        assert "#EXTM3U" in playlist
        assert "segment_00000.ts" in playlist

    def test_segment_count(self):
        gen = HLSGenerator(sr=22050)
        gen.segment(np.zeros(22050 * 12, dtype=np.float32))
        assert gen.segment_count == 2
