"""oauth2 domain events."""
from dataclasses import dataclass

@dataclass
class Oauth2Created:
    id: str
    timestamp: float

@dataclass
class Oauth2Updated:
    id: str
    changes: dict
