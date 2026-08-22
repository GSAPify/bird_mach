"""CLI wrapper for SDK operations."""
from __future__ import annotations
from bird_mach.sdk.client import MachClient, MachConfig

def run_analyze(path: str, api_key: str = "", base_url: str = "http://localhost:8000") -> dict:
    if not path or not path.strip():
        raise ValueError("path must not be empty")
    client = MachClient(MachConfig(base_url=base_url, api_key=api_key))
    client.connect()
    try:
        return client.analyze(path)
    finally:
        client.close()

def run_search(query: str, limit: int = 10, api_key: str = "") -> list[dict]:
    if not query or not query.strip():
        raise ValueError("query must not be empty")
    if limit < 1:
        raise ValueError("limit must be at least 1")
    client = MachClient(MachConfig(api_key=api_key))
    client.connect()
    try:
        return client.search(query, limit=limit)
    finally:
        client.close()
