"""i18n domain events."""
from dataclasses import dataclass

@dataclass
class I18NCreated:
    id: str
    timestamp: float

@dataclass
class I18NUpdated:
    id: str
    changes: dict
