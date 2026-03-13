"""Tests for constellation fingerprinting."""
import numpy as np
from bird_mach.fingerprint.shazam_like import ConstellationFingerprinter, Peak

class TestConstellationFingerprinter:
    def test_find_peaks(self):
        fp = ConstellationFingerprinter()
        spec = np.random.randn(64, 100).astype(np.float32) * 10
        peaks = fp.find_peaks(spec, threshold_db=-30)
        assert isinstance(peaks, list)
        assert all(isinstance(p, Peak) for p in peaks)

    def test_generate_hashes(self):
        fp = ConstellationFingerprinter(fan_out=3)
        peaks = [Peak(t, f, -10.0) for t in range(20) for f in range(5)]
        hashes = fp.generate_hashes(peaks[:30])
        assert len(hashes) > 0

    def test_hash_value_deterministic(self):
        from bird_mach.fingerprint.shazam_like import FingerprintHash
        h = FingerprintHash(anchor_freq=10, target_freq=20, delta_time=5, anchor_time=0)
        assert h.hash_value == h.hash_value
