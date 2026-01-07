"""locale domain events."""
from dataclasses import dataclass

@dataclass
class LocaleCreated:
    id: str
    timestamp: float

@dataclass
class LocaleUpdated:
    id: str
    changes: dict
