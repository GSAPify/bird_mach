"""Tests for cursor synchronization."""
import pytest

from bird_mach.collaboration.cursor_sync import CursorSyncManager


def test_update_and_remove():
    mgr = CursorSyncManager()
    mgr.update("u1", 1.5, is_playing=True)
    assert [c.position_s for c in mgr.get_all()] == [1.5]
    mgr.remove("u1")
    assert mgr.get_all() == []


def test_update_keeps_custom_color():
    mgr = CursorSyncManager()
    mgr.update("u1", 0.0).color = "#f97316"
    assert mgr.update("u1", 2.0).color == "#f97316"


def test_negative_position_rejected():
    with pytest.raises(ValueError):
        CursorSyncManager().update("u1", -1.0)
