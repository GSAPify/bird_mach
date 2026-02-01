"""video_thumb domain events."""
from dataclasses import dataclass

@dataclass
class VideoThumbCreated:
    id: str
    timestamp: float

@dataclass
class VideoThumbUpdated:
    id: str
    changes: dict
