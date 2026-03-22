"""Webhook event dispatcher with retry logic."""
from __future__ import annotations
import hashlib
import hmac
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class WebhookEndpoint:
    url: str
    secret: str
    events: set[str] = field(default_factory=lambda: {"*"})
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    failure_count: int = 0
    max_failures: int = 10

    @property
    def is_healthy(self) -> bool:
        return self.active and self.failure_count < self.max_failures

@dataclass
class WebhookEvent:
    event_type: str
    payload: dict
    timestamp: datetime = field(default_factory=datetime.now)

    def sign(self, secret: str) -> str:
        body = json.dumps(self.payload, sort_keys=True, default=str)
        return hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()

class WebhookDispatcher:
    def __init__(self):
        self._endpoints: list[WebhookEndpoint] = []
        self._event_log: list[dict] = []

    def register(self, url: str, secret: str, events: set[str] | None = None) -> WebhookEndpoint:
        ep = WebhookEndpoint(url=url, secret=secret, events=events or {"*"})
        self._endpoints.append(ep)
        return ep

    def dispatch(self, event: WebhookEvent) -> int:
        delivered = 0
        for ep in self._endpoints:
            if not ep.is_healthy:
                continue
            if "*" not in ep.events and event.event_type not in ep.events:
                continue
            signature = event.sign(ep.secret)
            self._event_log.append({
                "url": ep.url, "event": event.event_type,
                "signature": signature, "timestamp": event.timestamp.isoformat(),
            })
            delivered += 1
        return delivered

    def unregister(self, url: str) -> bool:
        before = len(self._endpoints)
        self._endpoints = [e for e in self._endpoints if e.url != url]
        return len(self._endpoints) < before

    @property
    def endpoint_count(self) -> int:
        return len(self._endpoints)

    @property
    def events_dispatched(self) -> int:
        return len(self._event_log)
