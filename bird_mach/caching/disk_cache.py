"""Disk-based cache for large analysis results."""
from __future__ import annotations
import hashlib
import json
import time
from pathlib import Path

class DiskCache:
    def __init__(self, cache_dir: Path, ttl_s: float = 3600.0):
        self._dir = cache_dir
        self._ttl = ttl_s
        self._dir.mkdir(parents=True, exist_ok=True)

    def _key_path(self, key: str) -> Path:
        h = hashlib.sha256(key.encode()).hexdigest()[:16]
        return self._dir / f"{h}.json"

    def get(self, key: str) -> dict | None:
        path = self._key_path(key)
        if not path.exists():
            return None
        data = json.loads(path.read_text())
        if time.time() > data.get("_expires_at", 0):
            path.unlink(missing_ok=True)
            return None
        # The filename is a truncated hash, so confirm the stored key really is
        # the one asked for rather than a collision.
        if data.get("_key") != key:
            return None
        return data.get("value")

    def set(self, key: str, value: dict, ttl_s: float | None = None) -> None:
        path = self._key_path(key)
        data = {"value": value,
                "_expires_at": time.time() + (self._ttl if ttl_s is None else ttl_s),
                "_key": key}
        path.write_text(json.dumps(data, default=str))

    def delete(self, key: str) -> bool:
        path = self._key_path(key)
        if path.exists():
            path.unlink()
            return True
        return False

    def clear(self) -> int:
        files = list(self._dir.glob("*.json"))
        for f in files:
            f.unlink()
        return len(files)

    @property
    def size(self) -> int:
        return len(list(self._dir.glob("*.json")))
