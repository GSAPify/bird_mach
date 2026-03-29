"""Async Mach SDK client."""
from __future__ import annotations
from bird_mach.sdk.client import MachConfig

class AsyncMachClient:
    """Async version of the Mach SDK client."""
    def __init__(self, config: MachConfig | None = None):
        self._config = config or MachConfig()
        self._connected = False

    async def connect(self) -> bool:
        self._connected = True
        return True

    async def analyze(self, audio_path: str, **params) -> dict:
        if not self._connected:
            raise ConnectionError("Not connected")
        return {"status": "queued", "path": audio_path}

    async def batch_analyze(self, paths: list[str]) -> list[dict]:
        return [{"path": p, "status": "queued"} for p in paths]

    async def close(self) -> None:
        self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected
