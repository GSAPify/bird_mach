"""terraform domain events."""
from dataclasses import dataclass

@dataclass
class TerraformCreated:
    id: str
    timestamp: float

@dataclass
class TerraformUpdated:
    id: str
    changes: dict
