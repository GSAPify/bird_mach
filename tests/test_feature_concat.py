"""Tests for bird_mach.feature_concat."""

import pytest
import numpy as np

from bird_mach.feature_concat import concat_features


class TestConcatFeatures:
    def test_single_1d(self):
        a = np.ones(10, dtype=np.float32)
        result = concat_features(a)
        assert result.shape == (10, 1)

    def test_two_1d(self):
        a = np.ones(10, dtype=np.float32)
        b = np.zeros(10, dtype=np.float32)
        result = concat_features(a, b)
        assert result.shape == (10, 2)

    def test_2d_transposed(self):
        a = np.ones((3, 20), dtype=np.float32)
        result = concat_features(a)
        assert result.shape == (20, 3)

    def test_min_alignment(self):
        a = np.ones(10, dtype=np.float32)
        b = np.ones(8, dtype=np.float32)
        result = concat_features(a, b, align="min")
        assert result.shape == (8, 2)

    def test_unknown_align_raises(self):
        # A typo like align="MINIMUM" previously fell through silently and
        # skipped truncation, returning mis-aligned or wrong-shaped results.
        a = np.ones(10, dtype=np.float32)
        with pytest.raises(ValueError, match="unknown align"):
            concat_features(a, align="MINIMUM")
