"""Tests for fingerprint matching."""
from bird_mach.fingerprint.matcher import FingerprintDB, MatchResult
from bird_mach.fingerprint.shazam_like import FingerprintHash

class TestFingerprintDB:
    def test_insert_and_count(self):
        db = FingerprintDB()
        hashes = [FingerprintHash(10, 20, 5, t) for t in range(10)]
        db.insert("track1", hashes, {"name": "Test"})
        assert db.track_count == 1
        assert db.hash_count == 10

    def test_search_finds_match(self):
        db = FingerprintDB()
        hashes = [FingerprintHash(i, i+10, 5, i) for i in range(20)]
        db.insert("track1", hashes)
        results = db.search(hashes, min_matches=3)
        assert len(results) >= 1
        assert results[0].track_id == "track1"

    def test_search_no_match(self):
        db = FingerprintDB()
        hashes = [FingerprintHash(100, 200, 50, 0)]
        results = db.search(hashes, min_matches=5)
        assert len(results) == 0
