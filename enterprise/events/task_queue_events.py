"""task_queue domain events."""
from dataclasses import dataclass

@dataclass
class TaskQueueCreated:
    id: str
    timestamp: float

@dataclass
class TaskQueueUpdated:
    id: str
    changes: dict
