# Collaboration API

## Rooms
```python
mgr = RoomManager()
room = mgr.create_room("Analysis Session", "user1")
room.add_participant("user2", "Alice")
```

## Annotations
Time-stamped markers on the audio waveform.

## Sharing
Generate secure links with password protection and expiry.

## Comments
Threaded discussions attached to analyses.

## Presence
Track who is online and where their cursor is.
