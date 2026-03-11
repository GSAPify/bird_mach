"""team_mgmt domain events."""
from dataclasses import dataclass

@dataclass
class TeamMgmtCreated:
    id: str
    timestamp: float

@dataclass
class TeamMgmtUpdated:
    id: str
    changes: dict
