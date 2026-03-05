"""Clustering wrappers for grouping audio frames or segments."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.cluster import KMeans, DBSCAN


@dataclass
class ClusterResult:
    """Result of clustering audio feature vectors."""

    labels: np.ndarray
    n_clusters: int
    inertia: float | None = None

    @property
    def label_counts(self) -> dict[int, int]:
        unique, counts = np.unique(self.labels, return_counts=True)
        return dict(zip(unique.tolist(), counts.tolist()))


def cluster_kmeans(
    X: np.ndarray, *, n_clusters: int = 5, random_state: int = 42
) -> ClusterResult:
    """Cluster feature vectors using K-Means."""
    n_clusters = min(n_clusters, X.shape[0])
    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    labels = model.fit_predict(X)
    return ClusterResult(
        labels=labels,
        n_clusters=n_clusters,
        inertia=float(model.inertia_),
    )


def cluster_dbscan(
    X: np.ndarray, *, eps: float = 0.5, min_samples: int = 5
) -> ClusterResult:
    """Cluster feature vectors using DBSCAN (density-based)."""
    model = DBSCAN(eps=eps, min_samples=min_samples)
    labels = model.fit_predict(X)
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    return ClusterResult(
        labels=labels,
        n_clusters=n_clusters,
    )
