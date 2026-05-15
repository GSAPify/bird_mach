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

def list_events(category: str = "all") -> dict[str, str]:
    # Copy: returning the live registries lets a caller mutate them globally.
    if category == "audio": return dict(AUDIO_EVENTS)
    if category == "collab": return dict(COLLAB_EVENTS)
    if category == "system": return dict(SYSTEM_EVENTS)
    return dict(ALL_EVENTS)
