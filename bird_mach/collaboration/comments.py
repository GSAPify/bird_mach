"""Threaded comments for audio analysis discussions."""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Comment:
    id: str
    user_id: str
    text: str
    parent_id: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    edited: bool = False

class CommentThread:
    def __init__(self):
        self._comments: dict[str, Comment] = {}

    def add(self, user_id: str, text: str, parent_id: str | None = None) -> Comment:
        c = Comment(id=str(uuid.uuid4())[:8], user_id=user_id, text=text, parent_id=parent_id)
        self._comments[c.id] = c
        return c

    def edit(self, comment_id: str, new_text: str) -> bool:
        c = self._comments.get(comment_id)
        if c:
            c.text = new_text
            c.edited = True
            return True
        return False

    def get_thread(self, parent_id: str | None = None) -> list[Comment]:
        return sorted(
            [c for c in self._comments.values() if c.parent_id == parent_id],
            key=lambda c: c.created_at,
        )

    @property
    def count(self) -> int:
        return len(self._comments)
