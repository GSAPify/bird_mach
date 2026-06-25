"""Tests for bird_mach.similarity."""

import numpy as np

from bird_mach.similarity import (
    cosine_similarity,
    euclidean_distance,
    manhattan_distance,
    feature_distance_matrix,
)


class TestCosineSimilarity:
    def test_identical_vectors(self):
        a = np.array([1.0, 2.0, 3.0])
        assert abs(cosine_similarity(a, a) - 1.0) < 1e-6

    def test_orthogonal_vectors(self):
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 1.0])
        assert abs(cosine_similarity(a, b)) < 1e-6

    def test_zero_vector(self):
        a = np.array([1.0, 2.0])
        z = np.zeros(2)
        assert cosine_similarity(a, z) == 0.0


class TestDistances:
    def test_euclidean_same_point(self):
        a = np.array([1.0, 2.0, 3.0])
        assert euclidean_distance(a, a) == 0.0

    def test_manhattan_known(self):
        a = np.array([0.0, 0.0])
        b = np.array([3.0, 4.0])
        assert manhattan_distance(a, b) == 7.0


class TestDistanceMatrix:
    def test_symmetric(self):
        X = np.random.default_rng(42).random((5, 3)).astype(np.float32)
        D = feature_distance_matrix(X, metric="euclidean")
        assert np.allclose(D, D.T)

    def test_diagonal_is_zero(self):
        X = np.random.default_rng(42).random((4, 2)).astype(np.float32)
        D = feature_distance_matrix(X)
        assert np.allclose(np.diag(D), 0.0)

    def test_cosine_metric(self):
        X = np.random.default_rng(0).random((4, 3)).astype(np.float32)
        D = feature_distance_matrix(X, metric="cosine")
        # cosine distance is 1 - similarity; diagonal should be ~0 (self-similarity=1)
        assert np.allclose(np.diag(D), 0.0, atol=1e-5)
        assert np.allclose(D, D.T, atol=1e-5)

    def test_manhattan_metric(self):
        X = np.array([[0.0, 0.0], [3.0, 4.0]], dtype=np.float32)
        D = feature_distance_matrix(X, metric="manhattan")
        assert abs(D[0, 1] - 7.0) < 1e-5
        assert abs(D[1, 0] - 7.0) < 1e-5

    def test_unknown_metric_raises(self):
        import pytest
        X = np.ones((3, 2), dtype=np.float32)
        with pytest.raises(ValueError, match="unknown metric"):
            feature_distance_matrix(X, metric="chebyshev")
