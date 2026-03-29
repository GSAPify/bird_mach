"""Tests for SDK client."""
import pytest
from bird_mach.sdk.client import MachClient, MachConfig

class TestMachClient:
    def test_connect(self):
        c = MachClient()
        assert c.connect()
        assert c.is_connected

    def test_analyze(self):
        c = MachClient()
        c.connect()
        result = c.analyze("test.wav", sr=22050)
        assert result["status"] == "queued"

    def test_analyze_disconnected(self):
        c = MachClient()
        with pytest.raises(ConnectionError):
            c.analyze("test.wav")

    def test_search(self):
        c = MachClient()
        c.connect()
        results = c.search("piano")
        assert len(results) > 0

    def test_close(self):
        c = MachClient()
        c.connect()
        c.close()
        assert not c.is_connected
