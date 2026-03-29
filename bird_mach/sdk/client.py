"""Mach SDK client for programmatic access."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class MachConfig:
    base_url: str = "http://localhost:8000"
    api_key: str = ""
    timeout_s: float = 30.0
    version: str = "v2"

class MachClient:
    """High-level SDK client for the Mach API."""
    def __init__(self, config: MachConfig | None = None):
        self._config = config or MachConfig()
        self._session_active = False

    def connect(self) -> bool:
        self._session_active = True
        return True

    def analyze(self, audio_path: str, **params) -> dict:
        if not self._session_active:
            raise ConnectionError("Not connected")
        return {"status": "queued", "path": audio_path, "params": params}

    def get_result(self, job_id: str) -> dict:
        return {"job_id": job_id, "status": "completed"}

    def search(self, query: str, limit: int = 20) -> list[dict]:
        return [{"id": f"result_{i}", "score": 1.0 - i * 0.1} for i in range(min(limit, 5))]

    def close(self) -> None:
        self._session_active = False

    @property
    def is_connected(self) -> bool:
        return self._session_active
