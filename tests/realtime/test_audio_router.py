"""Tests for AudioRouter."""
from bird_mach.realtime.audio_router import AudioRouter


class TestAudioRouter:
    def test_connect_and_gain(self):
        router = AudioRouter()
        router.connect("mic", "out", gain=0.5)
        assert router.get_destinations("mic") == ["out"]
        assert router.get_gain("mic", "out") == 0.5

    def test_reconnect_does_not_duplicate_route(self):
        router = AudioRouter()
        router.connect("mic", "out", gain=0.5)
        router.connect("mic", "out", gain=0.8)
        assert router.get_destinations("mic") == ["out"]
        assert router.get_gain("mic", "out") == 0.8

    def test_disconnect(self):
        router = AudioRouter()
        router.connect("mic", "out")
        router.disconnect("mic", "out")
        assert router.get_destinations("mic") == []
        assert router.get_gain("mic", "out") == 1.0

    def test_get_destinations_returns_copy(self):
        router = AudioRouter()
        router.connect("mic", "out")
        router.get_destinations("mic").append("rogue")
        assert router.get_destinations("mic") == ["out"]
