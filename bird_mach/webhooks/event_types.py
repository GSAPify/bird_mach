"""Standard webhook event type definitions."""
from __future__ import annotations

AUDIO_EVENTS = {
    "audio.uploaded": "Triggered when a new audio file is uploaded",
    "audio.analyzed": "Triggered when analysis completes",
    "audio.deleted": "Triggered when an audio file is deleted",
    "audio.transcoded": "Triggered when transcoding finishes",
}

COLLAB_EVENTS = {
    "room.created": "Triggered when a collaboration room is created",
    "room.joined": "Triggered when a user joins a room",
    "annotation.created": "Triggered when an annotation is added",
    "comment.created": "Triggered when a comment is posted",
}

SYSTEM_EVENTS = {
    "user.created": "Triggered when a new user is registered",
    "quota.exceeded": "Triggered when API quota is exceeded",
    "alert.fired": "Triggered when a monitoring alert fires",
}

ALL_EVENTS = {**AUDIO_EVENTS, **COLLAB_EVENTS, **SYSTEM_EVENTS}

def describe_event(event_type: str) -> str:
    return ALL_EVENTS.get(event_type, "Unknown event type")

EVENT_CATEGORIES = {
    "audio": AUDIO_EVENTS,
    "collab": COLLAB_EVENTS,
    "system": SYSTEM_EVENTS,
    "all": ALL_EVENTS,
}

def list_events(category: str = "all") -> dict[str, str]:
    # Copy: returning the live registries lets a caller mutate them globally.
    return dict(EVENT_CATEGORIES.get(category, ALL_EVENTS))
