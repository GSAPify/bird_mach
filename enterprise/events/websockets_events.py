"""websockets domain events."""
from dataclasses import dataclass

@dataclass
class WebsocketsCreated:
    id: str
    timestamp: float

@dataclass
class WebsocketsUpdated:
    id: str
    changes: dict
