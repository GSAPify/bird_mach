"""Cache key generation utilities."""
from __future__ import annotations
import hashlib
import json

def make_key(*parts: str) -> str:
    return ":".join(parts)

def content_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]

def params_hash(**kwargs) -> str:
    serialized = json.dumps(kwargs, sort_keys=True, default=str)
    return hashlib.md5(serialized.encode()).hexdigest()[:12]

def analysis_cache_key(file_hash: str, sr: int, hop: int, n_mels: int) -> str:
    return make_key("analysis", file_hash, f"sr{sr}", f"hop{hop}", f"mel{n_mels}")
