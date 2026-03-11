"""sse domain events."""
from dataclasses import dataclass

@dataclass
class SseCreated:
    id: str
    timestamp: float

@dataclass
class SseUpdated:
    id: str
    changes: dict
