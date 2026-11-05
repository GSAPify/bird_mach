"""Tests for webhook event type registry."""
import pytest

from bird_mach.webhooks.event_types import ALL_EVENTS, describe_event, list_events


def test_list_events_by_category():
    assert set(list_events("audio")) == {
        "audio.uploaded", "audio.analyzed", "audio.deleted", "audio.transcoded",
    }
    assert "room.created" in list_events("collab")
    assert "alert.fired" in list_events("system")
    assert list_events() == ALL_EVENTS


def test_list_events_returns_copy():
    list_events("audio")["audio.uploaded"] = "tampered"
    assert describe_event("audio.uploaded") != "tampered"


def test_describe_unknown_event():
    assert describe_event("nope") == "Unknown event type"


def test_list_events_rejects_unknown_category():
    with pytest.raises(ValueError, match="colab"):
        list_events("colab")
