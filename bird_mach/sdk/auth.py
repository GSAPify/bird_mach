"""SDK authentication helpers."""
from __future__ import annotations
import hashlib
import hmac
import time

class APIKeyAuth:
    """Authenticate SDK requests with an API key."""
    def __init__(self, api_key: str):
        self._key = api_key

    def headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._key}"}

    @property
    def is_configured(self) -> bool:
        return bool(self._key)

class HMACAuth:
    """Authenticate SDK requests with HMAC signing."""
    def __init__(self, key_id: str, secret: str):
        self._key_id = key_id
        self._secret = secret

    def sign(self, body: str) -> dict[str, str]:
        timestamp = str(int(time.time()))
        payload = f"{timestamp}.{body}"
        signature = hmac.new(
            self._secret.encode(), payload.encode(), hashlib.sha256
        ).hexdigest()
        return {
            "X-Key-Id": self._key_id,
            "X-Timestamp": timestamp,
            "X-Signature": signature,
        }
