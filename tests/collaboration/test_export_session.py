"""Tests for session export."""
import json

from bird_mach.collaboration.annotations import AnnotationStore
from bird_mach.collaboration.comments import CommentThread
from bird_mach.collaboration.export_session import SessionExporter


def test_export_includes_annotation_author_and_duration():
    store = AnnotationStore()
    store.add("r1", "u1", timestamp_s=2.0, duration_s=1.5, text="intro")
    thread = CommentThread()
    thread.add("u2", "nice")
    payload = json.loads(
        SessionExporter().export({"id": "r1"}, store.get_for_room("r1"), thread.get_thread())
    )
    assert payload["annotations"] == [
        {"user": "u1", "text": "intro", "time": 2.0, "duration": 1.5}
    ]
    assert payload["comments"] == [{"user": "u2", "text": "nice"}]
