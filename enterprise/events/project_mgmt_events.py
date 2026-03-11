"""project_mgmt domain events."""
from dataclasses import dataclass

@dataclass
class ProjectMgmtCreated:
    id: str
    timestamp: float

@dataclass
class ProjectMgmtUpdated:
    id: str
    changes: dict
