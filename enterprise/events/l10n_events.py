"""l10n domain events."""
from dataclasses import dataclass

@dataclass
class L10NCreated:
    id: str
    timestamp: float

@dataclass
class L10NUpdated:
    id: str
    changes: dict
