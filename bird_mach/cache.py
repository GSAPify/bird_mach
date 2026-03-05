"""Simple in-memory LRU cache for expensive audio computations."""

from __future__ import annotations

import hashlib
from collections import OrderedDict
from typing import Any


class AnalysisCache:
    """Thread-unsafe LRU cache keyed by content hash.

    Intended for caching UMAP embeddings or analysis summaries
    to avoid recomputing when the same file is uploaded twice.
    """

    def __init__(self, max_size: int = 32) -> None:
        self._max_size = max_size
        self._store: OrderedDict[str, Any] = OrderedDict()

    @staticmethod
    def content_hash(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()[:16]

    def get(self, key: str) -> Any | None:
        if key in self._store:
            self._store.move_to_end(key)
            return self._store[key]
        return None

    def put(self, key: str, value: Any) -> None:
        if key in self._store:
            self._store.move_to_end(key)
        self._store[key] = value
        while len(self._store) > self._max_size:
            self._store.popitem(last=False)

    def clear(self) -> None:
        self._store.clear()

    @property
    def size(self) -> int:
        return len(self._store)
