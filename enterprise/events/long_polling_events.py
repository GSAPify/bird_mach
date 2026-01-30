"""long_polling domain events."""
from dataclasses import dataclass

@dataclass
class LongPollingCreated:
    id: str
    timestamp: float

@dataclass
class LongPollingUpdated:
    id: str
    changes: dict
