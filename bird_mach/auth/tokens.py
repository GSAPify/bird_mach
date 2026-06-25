"""JWT issuance and verification, backed by PyJWT.

PyJWT is used rather than a hand-rolled HMAC: signature verification and
algorithm handling are exactly where hand-rolled JWT code grows
algorithm-confusion bugs. Tokens are HS256-signed with a server secret.

Two token types share one secret but are distinguished by a ``type`` claim so
a refresh token can never be replayed as an access token (and vice versa):

* ``access``  - short-lived, sent on every request.
* ``refresh`` - long-lived, exchanged for a new access token.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt

from bird_mach.exceptions import TokenError

ACCESS_TOKEN = "access"
REFRESH_TOKEN = "refresh"
_ALGORITHM = "HS256"


@dataclass(frozen=True)
class TokenClaims:
    """Decoded, verified claims for an authenticated principal."""

    subject: str
    role: str
    token_type: str
    expires_at: datetime


class TokenService:
    """Mints and verifies JWTs for a single signing secret.

    A weak/empty secret is rejected at construction: an HS256 token signed with
    a guessable secret is forgeable, so failing loudly at startup is safer than
    issuing tokens anyone can mint.
    """

    def __init__(
        self,
        secret: str,
        *,
        access_ttl_s: int = 900,
        refresh_ttl_s: int = 60 * 60 * 24 * 30,
        issuer: str = "mach",
    ) -> None:
        # RFC 7518 §3.2 requires an HS256 key at least as long as the hash
        # output (32 bytes); PyJWT warns below that. Enforce it up front so a
        # too-short secret fails at startup, not as a runtime warning.
        if not secret or len(secret.encode("utf-8")) < 32:
            raise ValueError("JWT secret must be at least 32 bytes")
        self._secret = secret
        self._access_ttl = access_ttl_s
        self._refresh_ttl = refresh_ttl_s
        self._issuer = issuer

    def _issue(self, subject: str, role: str, token_type: str, ttl_s: int) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": subject,
            "role": role,
            "type": token_type,
            "iss": self._issuer,
            "iat": now,
            "exp": now + timedelta(seconds=ttl_s),
        }
        return jwt.encode(payload, self._secret, algorithm=_ALGORITHM)

    def issue_access(self, subject: str, role: str) -> str:
        return self._issue(subject, role, ACCESS_TOKEN, self._access_ttl)

    def issue_refresh(self, subject: str, role: str) -> str:
        return self._issue(subject, role, REFRESH_TOKEN, self._refresh_ttl)

    def verify(self, token: str, *, expected_type: str = ACCESS_TOKEN) -> TokenClaims:
        """Decode and validate ``token``.

        Raises :class:`TokenError` for any failure (expired, bad signature,
        wrong issuer, or a token presented as the wrong type).
        """
        try:
            payload = jwt.decode(
                token,
                self._secret,
                algorithms=[_ALGORITHM],
                issuer=self._issuer,
                options={"require": ["exp", "sub", "iss"]},
            )
        except jwt.PyJWTError as exc:
            raise TokenError(str(exc)) from exc

        if payload.get("type") != expected_type:
            raise TokenError(
                f"expected {expected_type} token, got {payload.get('type')!r}"
            )
        return TokenClaims(
            subject=payload["sub"],
            role=payload.get("role", "user"),
            token_type=payload["type"],
            expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc),
        )
