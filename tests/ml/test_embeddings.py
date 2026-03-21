"""Tests for audio embeddings."""
import numpy as np
from bird_mach.ml.embeddings import AudioEmbedding, EmbeddingIndex

class TestAudioEmbedding:
    def test_embed(self):
        emb = AudioEmbedding(dim=64)
        y = np.random.randn(22050).astype(np.float32)
        vec = emb.embed(y)
        assert vec.shape == (64,)
        assert abs(np.linalg.norm(vec) - 1.0) < 0.01

    def test_similarity(self):
        emb = AudioEmbedding(dim=64)
        a = emb.embed(np.random.randn(22050).astype(np.float32))
        assert emb.similarity(a, a) > 0.99

class TestEmbeddingIndex:
    def test_add_and_search(self):
        idx = EmbeddingIndex()
        idx.add("a", np.array([1, 0, 0], dtype=np.float32))
        idx.add("b", np.array([0, 1, 0], dtype=np.float32))
        results = idx.search(np.array([1, 0.1, 0], dtype=np.float32))
        assert results[0][0] == "a"
