"""Audio genre/mood classifier."""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass

@dataclass
class Prediction:
    label: str
    confidence: float
    all_scores: dict[str, float]

class AudioClassifier:
    """Simple k-NN classifier for audio features."""
    def __init__(self, k: int = 5):
        if k < 1:
            raise ValueError("k must be at least 1")
        self._k = k
        self._features: list[np.ndarray] = []
        self._labels: list[str] = []

    def fit(self, features: list[np.ndarray], labels: list[str]) -> None:
        self._features = features
        self._labels = labels

    def predict(self, feature_vector: np.ndarray) -> Prediction:
        if not self._features:
            return Prediction("unknown", 0.0, {})
        distances = [float(np.linalg.norm(feature_vector - f)) for f in self._features]
        indices = np.argsort(distances)[:self._k]
        votes: dict[str, int] = {}
        for idx in indices:
            label = self._labels[idx]
            votes[label] = votes.get(label, 0) + 1
        best = max(votes, key=votes.get)
        # Divide by the neighbours actually found: with fewer samples than k
        # the confidences would otherwise never sum to 1.
        neighbours = max(len(indices), 1)
        scores = {k: v / neighbours for k, v in votes.items()}
        return Prediction(label=best, confidence=scores[best], all_scores=scores)

    @property
    def n_samples(self) -> int:
        return len(self._features)
