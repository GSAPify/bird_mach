"""Publish-subscribe event bus for decoupled communication."""
from __future__ import annotations
import logging
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class Event:
    name: str
    data: dict = field(default_factory=dict)
    source: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

class EventBus:
    def __init__(self):
        self._handlers: dict[str, list] = defaultdict(list)
        self._history: list[Event] = []
        self._max_history = 1000

    def on(self, event_name: str, handler: Callable[[Event], None]) -> None:
        if not callable(handler):
            raise TypeError("handler must be callable")
        self._handlers[event_name].append(handler)

    def off(self, event_name: str, handler: Callable[[Event], None]) -> None:
        # Indexing the defaultdict would create a permanent empty entry for an
        # event nobody ever subscribed to.
        if event_name not in self._handlers:
            return
        remaining = [h for h in self._handlers[event_name] if h != handler]
        if remaining:
            self._handlers[event_name] = remaining
        else:
            del self._handlers[event_name]

    def emit(self, event: Event) -> int:
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]
        handlers = self._handlers.get(event.name, []) + self._handlers.get("*", [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error("Handler error for %s: %s", event.name, e)
        return len(handlers)

    def recent_events(self, n: int = 20) -> list[Event]:
        # -0 == 0, so a plain [-n:] would return the whole history for n=0.
        if n <= 0:
            return []
        return list(reversed(self._history[-n:]))

    @property
    def handler_count(self) -> int:
        return sum(len(h) for h in self._handlers.values())
