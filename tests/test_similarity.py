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
