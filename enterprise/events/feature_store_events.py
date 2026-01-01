"""feature_store domain events."""
from dataclasses import dataclass

@dataclass
class FeatureStoreCreated:
    id: str
    timestamp: float

@dataclass
class FeatureStoreUpdated:
    id: str
    changes: dict
