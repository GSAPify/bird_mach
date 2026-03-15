"""Tests for feature hashing."""
import numpy as np
from bird_mach.fingerprint.feature_hash import feature_hash, hamming_distance

class TestFeatureHash:
    def test_deterministic(self):
        mfcc = np.random.default_rng(42).random((13, 100))
        assert feature_hash(mfcc) == feature_hash(mfcc)
    def test_hamming_same(self):
        assert hamming_distance("abc", "abc") == 0
    def test_hamming_diff(self):
        assert hamming_distance("abc", "xyz") == 3
