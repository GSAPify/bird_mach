"""docker_compose domain events."""
from dataclasses import dataclass

@dataclass
class DockerComposeCreated:
    id: str
    timestamp: float

@dataclass
class DockerComposeUpdated:
    id: str
    changes: dict
