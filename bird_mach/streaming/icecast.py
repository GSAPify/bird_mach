"""Icecast-compatible streaming client."""
from __future__ import annotations
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class IcecastConfig:
    host: str = "localhost"
    port: int = 8000
    mount: str = "/stream"
    password: str = ""
    bitrate: int = 128
    format: str = "mp3"

class IcecastClient:
    """Stream audio to an Icecast server."""
    def __init__(self, config: IcecastConfig):
        self._config = config
        self._connected = False
        self._bytes_sent = 0

    def connect(self) -> bool:
        logger.info("Connecting to icecast://%s:%d%s",
                   self._config.host, self._config.port, self._config.mount)
        self._connected = True
        return True

    def send(self, data: bytes) -> int:
        if not self._connected:
            raise ConnectionError("Not connected to Icecast")
        self._bytes_sent += len(data)
        return len(data)

    def disconnect(self) -> None:
        self._connected = False
        logger.info("Disconnected from Icecast (%d bytes sent)", self._bytes_sent)

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def bytes_sent(self) -> int:
        return self._bytes_sent
