"""mfa domain events."""
from dataclasses import dataclass

@dataclass
class MfaCreated:
    id: str
    timestamp: float

@dataclass
class MfaUpdated:
    id: str
    changes: dict
