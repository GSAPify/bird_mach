"""Tests for feature extraction."""
import numpy as np
from bird_mach.ml.feature_extractor import AudioFeatureExtractor

class TestFeatureExtractor:
    def test_extract(self):
        ext = AudioFeatureExtractor()
        y = np.random.randn(22050).astype(np.float32)
        features = ext.extract(y)
        assert features.spectral_centroid > 0
        assert features.rms_energy > 0

    def test_to_vector(self):
        ext = AudioFeatureExtractor()
        y = np.random.randn(22050).astype(np.float32)
        vec = ext.extract(y).to_vector()
        assert vec.ndim == 1
        assert len(vec) == 13 + 13 + 12 + 5
