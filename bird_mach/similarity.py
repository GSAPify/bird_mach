"""Distance and similarity metrics for audio feature vectors."""

from __future__ import annotations

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two 1-D vectors."""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a < 1e-10 or norm_b < 1e-10:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    """Compute Euclidean distance between two vectors."""
    return float(np.linalg.norm(a - b))


def manhattan_distance(a: np.ndarray, b: np.ndarray) -> float:
    """Compute Manhattan (L1) distance between two vectors."""
    return float(np.sum(np.abs(a - b)))


def feature_distance_matrix(X: np.ndarray, metric: str = "euclidean") -> np.ndarray:
    """Compute pairwise distance matrix for rows of X.

    Args:
        X: Feature matrix of shape (n_samples, n_features).
        metric: One of "euclidean", "cosine", "manhattan".

    Returns:
        Symmetric distance matrix of shape (n_samples, n_samples).
    """
    n = X.shape[0]
    D = np.zeros((n, n), dtype=np.float32)
    metric_fn = {
        "euclidean": euclidean_distance,
        "cosine": lambda a, b: 1.0 - cosine_similarity(a, b),
        "manhattan": manhattan_distance,
    }.get(metric, euclidean_distance)

    for i in range(n):
        for j in range(i + 1, n):
            d = metric_fn(X[i], X[j])
            D[i, j] = d
            D[j, i] = d
    return D
