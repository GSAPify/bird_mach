"""currency domain events."""
from dataclasses import dataclass

@dataclass
class CurrencyCreated:
    id: str
    timestamp: float

@dataclass
class CurrencyUpdated:
    id: str
    changes: dict
