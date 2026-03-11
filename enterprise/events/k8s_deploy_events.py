"""k8s_deploy domain events."""
from dataclasses import dataclass

@dataclass
class K8SDeployCreated:
    id: str
    timestamp: float

@dataclass
class K8SDeployUpdated:
    id: str
    changes: dict
