"""Collaboration rooms for shared audio analysis sessions."""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Participant:
    user_id: str
    display_name: str
    role: str = "viewer"
    joined_at: datetime = field(default_factory=datetime.now)
    cursor_position: float = 0.0

@dataclass
class CollabRoom:
    room_id: str
    name: str
    owner_id: str
    created_at: datetime = field(default_factory=datetime.now)
    participants: dict[str, Participant] = field(default_factory=dict)
    audio_file_id: str | None = None
    is_locked: bool = False

    def add_participant(self, user_id: str, name: str, role: str = "viewer") -> Participant:
        if self.is_locked and role != "admin":
            raise PermissionError("Room is locked")
        p = Participant(user_id=user_id, display_name=name, role=role)
        self.participants[user_id] = p
        return p

    def remove_participant(self, user_id: str) -> None:
        self.participants.pop(user_id, None)

    @property
    def participant_count(self) -> int:
        return len(self.participants)

class RoomManager:
    def __init__(self):
        self._rooms: dict[str, CollabRoom] = {}

    def create_room(self, name: str, owner_id: str) -> CollabRoom:
        room_id = str(uuid.uuid4())[:8]
        room = CollabRoom(room_id=room_id, name=name, owner_id=owner_id)
        self._rooms[room_id] = room
        return room

    def get_room(self, room_id: str) -> CollabRoom | None:
        return self._rooms.get(room_id)

    def delete_room(self, room_id: str) -> bool:
        return self._rooms.pop(room_id, None) is not None

    @property
    def active_rooms(self) -> int:
        return len(self._rooms)
