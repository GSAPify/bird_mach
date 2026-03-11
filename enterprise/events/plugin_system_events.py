"""plugin_system domain events."""
from dataclasses import dataclass

@dataclass
class PluginSystemCreated:
    id: str
    timestamp: float

@dataclass
class PluginSystemUpdated:
    id: str
    changes: dict
