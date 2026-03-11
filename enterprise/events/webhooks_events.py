"""webhooks domain events."""
from dataclasses import dataclass

@dataclass
class WebhooksCreated:
    id: str
    timestamp: float

@dataclass
class WebhooksUpdated:
    id: str
    changes: dict
