"""Simple in-memory LRU cache for expensive audio computations."""

from __future__ import annotations

import hashlib
import threading
from collections import OrderedDict
from typing import Any


class AnalysisCache:
    """LRU cache keyed by content hash.

    Intended for caching UMAP embeddings or analysis summaries
    to avoid recomputing when the same file is uploaded twice.
    """

    def __init__(self, max_size: int = 32) -> None:
        if max_size < 1:
            raise ValueError(f"max_size must be at least 1, got {max_size}")
        self._max_size = max_size
        self._store: OrderedDict[str, Any] = OrderedDict()
        self._lock = threading.Lock()

    @staticmethod
    def content_hash(data: bytes) -> str:
        if not data:
            raise ValueError("content_hash requires non-empty data")
        return hashlib.sha256(data).hexdigest()[:16]

    def get(self, key: str) -> Any | None:
        with self._lock:
            if key in self._store:
                self._store.move_to_end(key)
                return self._store[key]
            return None

    def put(self, key: str, value: Any) -> None:
        with self._lock:
            if key in self._store:
                self._store.move_to_end(key)
            self._store[key] = value
            while len(self._store) > self._max_size:
                self._store.popitem(last=False)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._store)
