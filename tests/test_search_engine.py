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

    def test_empty_query_returns_empty(self):
        engine = AudioSearchEngine()
        engine.index("a1", "Piano", "piano music")
        assert engine.search("") == []
        assert engine.search("   ") == []

    def test_limit_respected(self):
        engine = AudioSearchEngine()
        for i in range(5):
            engine.index(f"a{i}", f"Track {i}", "piano music")
        results = engine.search("piano", limit=2)
        assert len(results) == 2

    def test_negative_limit_raises(self):
        import pytest
        engine = AudioSearchEngine()
        engine.index("a1", "Piano", "piano music")
        with pytest.raises(ValueError, match="non-negative"):
            engine.search("piano", limit=-1)

    def test_remove_nonexistent_returns_false(self):
        engine = AudioSearchEngine()
        assert engine.remove("does-not-exist") is False

    def test_snippet_included_in_result(self):
        engine = AudioSearchEngine()
        engine.index("a1", "Piano Concerto", "a grand piano in a concert hall")
        results = engine.search("piano")
        assert results[0].snippet != ""
