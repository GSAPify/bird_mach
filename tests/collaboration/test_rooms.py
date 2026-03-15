"""Tests for collaboration rooms."""
import pytest
from bird_mach.collaboration.rooms import RoomManager, CollabRoom

class TestRoomManager:
    def test_create_room(self):
        mgr = RoomManager()
        room = mgr.create_room("Test Room", "user1")
        assert room.name == "Test Room"
        assert mgr.active_rooms == 1

    def test_delete_room(self):
        mgr = RoomManager()
        room = mgr.create_room("Test", "user1")
        assert mgr.delete_room(room.room_id)
        assert mgr.active_rooms == 0

    def test_add_participant(self):
        mgr = RoomManager()
        room = mgr.create_room("Test", "user1")
        room.add_participant("user2", "Alice")
        assert room.participant_count == 1

    def test_locked_room_rejects(self):
        mgr = RoomManager()
        room = mgr.create_room("Test", "user1")
        room.is_locked = True
        with pytest.raises(PermissionError):
            room.add_participant("user2", "Bob")
