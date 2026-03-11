"""canary_deploy domain events."""
from dataclasses import dataclass

@dataclass
class CanaryDeployCreated:
    id: str
    timestamp: float

@dataclass
class CanaryDeployUpdated:
    id: str
    changes: dict
