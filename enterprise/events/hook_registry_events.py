"""hook_registry domain events."""
from dataclasses import dataclass

@dataclass
class HookRegistryCreated:
    id: str
    timestamp: float

@dataclass
class HookRegistryUpdated:
    id: str
    changes: dict
