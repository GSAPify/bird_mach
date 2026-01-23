"""helm_charts domain events."""
from dataclasses import dataclass

@dataclass
class HelmChartsCreated:
    id: str
    timestamp: float

@dataclass
class HelmChartsUpdated:
    id: str
    changes: dict
