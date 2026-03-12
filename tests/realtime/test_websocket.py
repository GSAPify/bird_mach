"""Tests for WebSocket manager."""
import pytest
import asyncio
from bird_mach.realtime.websocket import AudioWebSocketManager

class TestAudioWebSocketManager:
    def test_register(self):
        mgr = AudioWebSocketManager()
        client = mgr.register("c1", 1000.0)
        assert mgr.client_count == 1
        assert client.client_id == "c1"

    def test_unregister(self):
        mgr = AudioWebSocketManager()
        mgr.register("c1", 1000.0)
        mgr.unregister("c1")
        assert mgr.client_count == 0

    def test_max_clients(self):
        mgr = AudioWebSocketManager(max_clients=2)
        mgr.register("c1", 1.0)
        mgr.register("c2", 2.0)
        with pytest.raises(ConnectionError):
            mgr.register("c3", 3.0)

    def test_subscribe_channel(self):
        mgr = AudioWebSocketManager()
        mgr.register("c1", 1.0)
        mgr.subscribe("c1", "audio")
        assert "c1" in mgr.get_channel_clients("audio")

    @pytest.mark.asyncio
    async def test_broadcast(self):
        mgr = AudioWebSocketManager()
        mgr.register("c1", 1.0)
        mgr.subscribe("c1", "audio")
        sent = await mgr.broadcast("audio", {"rms": 0.5})
        assert sent == 1
