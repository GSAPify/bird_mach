"""Tests for chromaprint fingerprinting."""
import numpy as np
from bird_mach.fingerprint.chromaprint import AudioFingerprinter

class TestAudioFingerprinter:
    def test_fingerprint_returns_hash(self):
        fp = AudioFingerprinter(sr=22050)
        y = np.random.randn(22050).astype(np.float32)
        result = fp.fingerprint(y)
        assert isinstance(result, str)
        assert len(result) == 64

    def test_same_audio_same_fingerprint(self):
        fp = AudioFingerprinter()
        y = np.random.default_rng(42).standard_normal(22050).astype(np.float32)
        assert fp.fingerprint(y) == fp.fingerprint(y)

    def test_empty_audio(self):
        fp = AudioFingerprinter()
        assert fp.fingerprint(np.array([], dtype=np.float32)) == ""

    def test_similarity_identical(self):
        fp = AudioFingerprinter()
        h = "a" * 64
        assert fp.similarity(h, h) == 1.0
