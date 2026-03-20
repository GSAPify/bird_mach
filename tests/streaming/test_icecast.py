"""Tests for Icecast client."""
import pytest
from bird_mach.streaming.icecast import IcecastClient, IcecastConfig

class TestIcecastClient:
    def test_connect(self):
        client = IcecastClient(IcecastConfig())
        assert client.connect()
        assert client.is_connected

    def test_send(self):
        client = IcecastClient(IcecastConfig())
        client.connect()
        sent = client.send(b"audio-data")
        assert sent == 10
        assert client.bytes_sent == 10

    def test_send_disconnected_raises(self):
        client = IcecastClient(IcecastConfig())
        with pytest.raises(ConnectionError):
            client.send(b"data")

    def test_disconnect(self):
        client = IcecastClient(IcecastConfig())
        client.connect()
        client.disconnect()
        assert not client.is_connected
