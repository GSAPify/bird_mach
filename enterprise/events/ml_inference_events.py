"""ml_inference domain events."""
from dataclasses import dataclass

@dataclass
class MlInferenceCreated:
    id: str
    timestamp: float

@dataclass
class MlInferenceUpdated:
    id: str
    changes: dict
