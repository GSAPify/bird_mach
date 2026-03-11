"""model_registry domain events."""
from dataclasses import dataclass

@dataclass
class ModelRegistryCreated:
    id: str
    timestamp: float

@dataclass
class ModelRegistryUpdated:
    id: str
    changes: dict
