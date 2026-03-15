"""Audio fingerprint matching and search."""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass

@dataclass
class MatchResult:
    track_id: str
    confidence: float
    offset: int
    match_count: int

class FingerprintDB:
    """In-memory fingerprint database for audio matching."""

    def __init__(self):
        self._index: dict[int, list[tuple[str, int]]] = defaultdict(list)
        self._tracks: dict[str, dict] = {}

    def insert(self, track_id: str, hashes: list, metadata: dict | None = None):
        self._tracks[track_id] = metadata or {}
        for h in hashes:
            self._index[h.hash_value].append((track_id, h.anchor_time))

    def search(self, query_hashes: list, min_matches: int = 5) -> list[MatchResult]:
        candidates: dict[str, list[int]] = defaultdict(list)
        for h in query_hashes:
            for track_id, stored_time in self._index.get(h.hash_value, []):
                offset = h.anchor_time - stored_time
                candidates[track_id].append(offset)

        results = []
        for track_id, offsets in candidates.items():
            if len(offsets) < min_matches:
                continue
            from collections import Counter
            offset_counts = Counter(offsets)
            best_offset, best_count = offset_counts.most_common(1)[0]
            confidence = best_count / max(len(query_hashes), 1)
            results.append(MatchResult(
                track_id=track_id, confidence=confidence,
                offset=best_offset, match_count=best_count,
            ))
        results.sort(key=lambda r: r.confidence, reverse=True)
        return results

    @property
    def track_count(self) -> int:
        return len(self._tracks)

    @property
    def hash_count(self) -> int:
        return sum(len(v) for v in self._index.values())
