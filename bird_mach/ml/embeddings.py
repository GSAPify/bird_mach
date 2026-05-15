"""Audio embedding generation for similarity search."""
from __future__ import annotations
import numpy as np

class AudioEmbedding:
    """Generate fixed-length embeddings from audio for vector search."""
    def __init__(self, dim: int = 128, sr: int = 22050):
        if dim < 1:
            raise ValueError("dim must be at least 1")
        if sr <= 0:
            raise ValueError("sr must be positive")
        self._dim = dim
        self._sr = sr

    def embed(self, y: np.ndarray) -> np.ndarray:
        n_frames = max(1, len(y) // self._sr)
        features = []
        for i in range(n_frames):
            chunk = y[i * self._sr:(i + 1) * self._sr]
            spectrum = np.abs(np.fft.rfft(chunk))[:self._dim]
            if len(spectrum) < self._dim:
                spectrum = np.pad(spectrum, (0, self._dim - len(spectrum)))
            features.append(spectrum)
        embedding = np.mean(features, axis=0)
        norm = np.linalg.norm(embedding) + 1e-10
        return (embedding / norm).astype(np.float32)

    def similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        if emb1.shape != emb2.shape:
            raise ValueError("embeddings must have the same shape")
        return float(np.dot(emb1, emb2))

class EmbeddingIndex:
    """Simple brute-force index for audio embeddings."""
    def __init__(self):
        self._embeddings: dict[str, np.ndarray] = {}

    def add(self, doc_id: str, embedding: np.ndarray) -> None:
        self._embeddings[doc_id] = embedding

    def search(self, query: np.ndarray, top_k: int = 5) -> list[tuple[str, float]]:
        scores = [(did, float(np.dot(query, emb)))
                  for did, emb in self._embeddings.items()]
        scores.sort(key=lambda x: -x[1])
        return scores[:top_k]

    @property
    def size(self) -> int:
        return len(self._embeddings)
