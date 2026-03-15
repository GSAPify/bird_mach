"""Audio deduplication using fingerprint comparison."""
from __future__ import annotations
from bird_mach.fingerprint.chromaprint import AudioFingerprinter
import numpy as np

class AudioDeduplicator:
    """Detect duplicate audio files using fingerprint similarity."""
    def __init__(self, threshold: float = 0.9):
        self._fp = AudioFingerprinter()
        self._threshold = threshold
        self._hashes: dict[str, str] = {}

    def add(self, file_id: str, audio: np.ndarray) -> str:
        h = self._fp.fingerprint(audio)
        self._hashes[file_id] = h
        return h

    def find_duplicates(self, file_id: str) -> list[tuple[str, float]]:
        target = self._hashes.get(file_id, "")
        if not target:
            return []
        dupes = []
        for fid, h in self._hashes.items():
            if fid == file_id:
                continue
            sim = self._fp.similarity(target, h)
            if sim >= self._threshold:
                dupes.append((fid, sim))
        return sorted(dupes, key=lambda x: -x[1])
