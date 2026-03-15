"""Tests for search engine."""
from bird_mach.search_engine import AudioSearchEngine

class TestAudioSearchEngine:
    def test_index_and_search(self):
        engine = AudioSearchEngine()
        engine.index("a1", "Piano Sonata", "classical piano music")
        results = engine.search("piano")
        assert len(results) == 1
        assert results[0].id == "a1"

    def test_no_match(self):
        engine = AudioSearchEngine()
        engine.index("a1", "Guitar", "rock guitar solo")
        assert len(engine.search("violin")) == 0

    def test_ranking(self):
        engine = AudioSearchEngine()
        engine.index("a1", "Piano", "piano piano piano")
        engine.index("a2", "Guitar with Piano", "guitar")
        results = engine.search("piano")
        assert results[0].id == "a1"

    def test_remove(self):
        engine = AudioSearchEngine()
        engine.index("a1", "Test", "test content")
        engine.remove("a1")
        assert engine.document_count == 0
