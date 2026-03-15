"""Export collaboration sessions for archival."""
from __future__ import annotations
import json
from datetime import datetime

class SessionExporter:
    """Export a collaboration session to JSON."""
    def export(self, room_data: dict, annotations: list, comments: list) -> str:
        payload = {
            "exported_at": datetime.now().isoformat(),
            "room": room_data,
            "annotations": [{"text": a.text, "time": a.timestamp_s} for a in annotations],
            "comments": [{"user": c.user_id, "text": c.text} for c in comments],
            "version": "1.0",
        }
        return json.dumps(payload, indent=2, default=str)
