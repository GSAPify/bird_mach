"""Time-stamped annotations for collaborative audio review."""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Annotation:
    id: str
    user_id: str
    timestamp_s: float
    duration_s: float
    text: str
    color: str = "#38bdf8"
    created_at: datetime = field(default_factory=datetime.now)
    reactions: dict[str, list[str]] = field(default_factory=dict)

    def add_reaction(self, emoji: str, user_id: str) -> None:
        self.reactions.setdefault(emoji, [])
        if user_id not in self.reactions[emoji]:
            self.reactions[emoji].append(user_id)

class AnnotationStore:
    def __init__(self):
        self._annotations: dict[str, list[Annotation]] = {}

    def add(self, room_id: str, user_id: str, timestamp_s: float,
            duration_s: float, text: str, color: str = "#38bdf8") -> Annotation:
        ann = Annotation(
            id=str(uuid.uuid4())[:8], user_id=user_id,
            timestamp_s=timestamp_s, duration_s=duration_s,
            text=text, color=color,
        )
        self._annotations.setdefault(room_id, []).append(ann)
        return ann

    def get_for_room(self, room_id: str) -> list[Annotation]:
        return sorted(
            self._annotations.get(room_id, []),
            key=lambda a: a.timestamp_s,
        )

    def delete(self, room_id: str, annotation_id: str) -> bool:
        anns = self._annotations.get(room_id, [])
        for i, a in enumerate(anns):
            if a.id == annotation_id:
                anns.pop(i)
                return True
        return False
