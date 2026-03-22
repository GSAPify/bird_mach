"""Tests for event bus."""
from bird_mach.events.bus import EventBus, Event

class TestEventBus:
    def test_emit(self):
        bus = EventBus()
        received = []
        bus.on("upload", lambda e: received.append(e))
        bus.emit(Event("upload", {"file": "test.wav"}))
        assert len(received) == 1

    def test_wildcard(self):
        bus = EventBus()
        received = []
        bus.on("*", lambda e: received.append(e))
        bus.emit(Event("anything", {}))
        assert len(received) == 1

    def test_off(self):
        bus = EventBus()
        handler = lambda e: None
        bus.on("test", handler)
        bus.off("test", handler)
        assert bus.emit(Event("test", {})) == 0

    def test_history(self):
        bus = EventBus()
        bus.emit(Event("a", {}))
        bus.emit(Event("b", {}))
        assert len(bus.recent_events()) == 2
