"""Tests for bird_mach.clustering."""

import numpy as np

from bird_mach.clustering import cluster_kmeans, cluster_dbscan, ClusterResult


class TestKMeans:
    def test_returns_cluster_result(self):
        X = np.random.default_rng(42).random((50, 3)).astype(np.float32)
        result = cluster_kmeans(X, n_clusters=3)
        assert isinstance(result, ClusterResult)
        assert result.n_clusters == 3
        assert len(result.labels) == 50

    def test_clamps_n_clusters(self):
        X = np.random.default_rng(42).random((3, 2)).astype(np.float32)
        result = cluster_kmeans(X, n_clusters=10)
        assert result.n_clusters <= 3

    def test_label_counts_sum(self):
        X = np.random.default_rng(42).random((20, 4)).astype(np.float32)
        result = cluster_kmeans(X, n_clusters=2)
        assert sum(result.label_counts.values()) == 20


class TestDBSCAN:
    def test_returns_cluster_result(self):
        X = np.random.default_rng(42).random((30, 2)).astype(np.float32)
        result = cluster_dbscan(X, eps=0.3, min_samples=3)
        assert isinstance(result, ClusterResult)
        assert len(result.labels) == 30
