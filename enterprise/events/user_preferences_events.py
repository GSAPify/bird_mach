"""user_preferences domain events."""
from dataclasses import dataclass

@dataclass
class UserPreferencesCreated:
    id: str
    timestamp: float

@dataclass
class UserPreferencesUpdated:
    id: str
    changes: dict
