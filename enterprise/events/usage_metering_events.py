"""usage_metering domain events."""
from dataclasses import dataclass

@dataclass
class UsageMeteringCreated:
    id: str
    timestamp: float

@dataclass
class UsageMeteringUpdated:
    id: str
    changes: dict
