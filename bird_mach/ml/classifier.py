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
        scores = {k: v / self._k for k, v in votes.items()}
        return Prediction(label=best, confidence=scores[best], all_scores=scores)

    @property
    def n_samples(self) -> int:
        return len(self._features)
