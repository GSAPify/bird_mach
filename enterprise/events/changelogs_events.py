"""changelogs domain events."""
from dataclasses import dataclass

@dataclass
class ChangelogsCreated:
    id: str
    timestamp: float

@dataclass
class ChangelogsUpdated:
    id: str
    changes: dict
