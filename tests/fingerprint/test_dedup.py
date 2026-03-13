"""Tests for deduplication."""
import numpy as np
from bird_mach.fingerprint.dedup import AudioDeduplicator
class TestDedup:
    def test_add(self):
        dd = AudioDeduplicator()
        h = dd.add("f1", np.random.randn(22050).astype(np.float32))
        assert isinstance(h, str)
    def test_same_audio_is_duplicate(self):
        dd = AudioDeduplicator(threshold=0.5)
        audio = np.random.default_rng(42).standard_normal(22050).astype(np.float32)
        dd.add("f1", audio)
        dd.add("f2", audio)
        dupes = dd.find_duplicates("f1")
        assert len(dupes) >= 1
