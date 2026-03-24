# Webhooks

## Event Types
- `audio.uploaded` — New audio file uploaded
- `audio.analyzed` — Analysis completed
- `audio.deleted` — Audio file deleted
- `room.created` — Collaboration room created
- `annotation.created` — New annotation added
- `quota.exceeded` — API quota exceeded

## Security
All webhook payloads are signed with HMAC-SHA256.

## Retry Policy
Failed deliveries retry with exponential backoff (max 5 retries).

## Configuration
```python
from bird_mach.webhooks.dispatcher import WebhookDispatcher, WebhookEvent
dispatcher = WebhookDispatcher()
dispatcher.register("https://your-app.com/hook", "your-secret", {"audio.analyzed"})
dispatcher.dispatch(WebhookEvent("audio.analyzed", {"id": "abc"}))
```
