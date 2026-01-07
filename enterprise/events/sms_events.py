"""sms domain events."""
from dataclasses import dataclass

@dataclass
class SmsCreated:
    id: str
    timestamp: float

@dataclass
class SmsUpdated:
    id: str
    changes: dict
