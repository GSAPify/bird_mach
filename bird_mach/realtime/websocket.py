"""WebSocket protocol handler for streaming audio data."""
from __future__ import annotations
import json
import logging
import asyncio
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class WSClient:
    """Represents a connected WebSocket client."""
    client_id: str
    connected_at: float
    subscriptions: set[str] = field(default_factory=set)
    frames_sent: int = 0

class AudioWebSocketManager:
    """Manage WebSocket connections for real-time audio streaming."""

    def __init__(self, max_clients: int = 100) -> None:
        self._clients: dict[str, WSClient] = {}
        self._max_clients = max_clients
        self._channels: dict[str, set[str]] = {}

    @property
    def client_count(self) -> int:
        return len(self._clients)

    def register(self, client_id: str, timestamp: float) -> WSClient:
        if len(self._clients) >= self._max_clients:
            raise ConnectionError("Max clients reached")
        client = WSClient(client_id=client_id, connected_at=timestamp)
        self._clients[client_id] = client
        logger.info("Client %s connected (%d total)", client_id, self.client_count)
        return client

    def unregister(self, client_id: str) -> None:
        client = self._clients.pop(client_id, None)
        if client:
            for ch in client.subscriptions:
                self._channels.get(ch, set()).discard(client_id)
            logger.info("Client %s disconnected", client_id)

    def subscribe(self, client_id: str, channel: str) -> None:
        if client_id in self._clients:
            self._clients[client_id].subscriptions.add(channel)
            self._channels.setdefault(channel, set()).add(client_id)

    def unsubscribe(self, client_id: str, channel: str) -> None:
        if client_id in self._clients:
            self._clients[client_id].subscriptions.discard(channel)
            self._channels.get(channel, set()).discard(client_id)

    def get_channel_clients(self, channel: str) -> list[str]:
        return list(self._channels.get(channel, set()))

    async def broadcast(self, channel: str, data: dict) -> int:
        clients = self.get_channel_clients(channel)
        msg = json.dumps(data)
        sent = 0
        for cid in clients:
            if cid in self._clients:
                self._clients[cid].frames_sent += 1
                sent += 1
        return sent
