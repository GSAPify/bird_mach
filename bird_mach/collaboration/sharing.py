"""Audio sharing and link generation."""
from __future__ import annotations
import hashlib
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class ShareLink:
    token: str
    audio_id: str
    created_by: str
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime | None = None
    max_views: int | None = None
    view_count: int = 0
    password_hash: str | None = None

    @property
    def is_expired(self) -> bool:
        if self.expires_at and datetime.now() > self.expires_at:
            return True
        if self.max_views and self.view_count >= self.max_views:
            return True
        return False

class SharingService:
    def __init__(self):
        self._links: dict[str, ShareLink] = {}

    def create_link(
        self, audio_id: str, user_id: str,
        expires_in_hours: int | None = None,
        max_views: int | None = None,
        password: str | None = None,
    ) -> ShareLink:
        token = secrets.token_urlsafe(16)
        expires = None
        if expires_in_hours:
            expires = datetime.now() + timedelta(hours=expires_in_hours)
        pw_hash = hashlib.sha256(password.encode()).hexdigest() if password else None
        link = ShareLink(
            token=token, audio_id=audio_id, created_by=user_id,
            expires_at=expires, max_views=max_views, password_hash=pw_hash,
        )
        self._links[token] = link
        return link

    def access(self, token: str, password: str | None = None) -> ShareLink | None:
        link = self._links.get(token)
        if not link or link.is_expired:
            return None
        if link.password_hash:
            if not password or hashlib.sha256(password.encode()).hexdigest() != link.password_hash:
                return None
        link.view_count += 1
        return link

    def revoke(self, token: str) -> bool:
        return self._links.pop(token, None) is not None
