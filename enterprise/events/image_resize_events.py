"""image_resize domain events."""
from dataclasses import dataclass

@dataclass
class ImageResizeCreated:
    id: str
    timestamp: float

@dataclass
class ImageResizeUpdated:
    id: str
    changes: dict
