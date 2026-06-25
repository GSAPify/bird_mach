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

import hashlib
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt

from bird_mach.exceptions import TokenError

ACCESS_TOKEN = "access"
REFRESH_TOKEN = "refresh"
PASSWORD_RESET = "password_reset"
VERIFY_EMAIL = "verify_email"
_ALGORITHM = "HS256"


def _hash_fingerprint(password_hash: str) -> str:
    """Short, non-reversible fingerprint of a stored password hash.

    Embedded in reset tokens so a token becomes invalid the moment the
    password changes — making reset tokens effectively single-use without a
    server-side token store.
    """
    return hashlib.sha256(password_hash.encode("utf-8")).hexdigest()[:16]


@dataclass(frozen=True)
class TokenClaims:
    """Decoded, verified claims for an authenticated principal."""

    subject: str
    role: str
    token_type: str
    expires_at: datetime
    # Unique token id, used to revoke a specific token (e.g. on logout).
    jti: str = ""


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
            "jti": uuid.uuid4().hex,
            "iss": self._issuer,
            "iat": now,
            "exp": now + timedelta(seconds=ttl_s),
        }
        return jwt.encode(payload, self._secret, algorithm=_ALGORITHM)

    def issue_access(self, subject: str, role: str) -> str:
        return self._issue(subject, role, ACCESS_TOKEN, self._access_ttl)

    def issue_refresh(self, subject: str, role: str) -> str:
        return self._issue(subject, role, REFRESH_TOKEN, self._refresh_ttl)

    def issue_password_reset(
        self, subject: str, password_hash: str, *, ttl_s: int = 3600
    ) -> str:
        """Issue a short-lived reset token bound to the current password hash."""
        now = datetime.now(timezone.utc)
        payload = {
            "sub": subject,
            "type": PASSWORD_RESET,
            "pwf": _hash_fingerprint(password_hash),
            "iss": self._issuer,
            "iat": now,
            "exp": now + timedelta(seconds=ttl_s),
        }
        return jwt.encode(payload, self._secret, algorithm=_ALGORITHM)

    def issue_email_verification(self, subject: str, *, ttl_s: int = 60 * 60 * 24) -> str:
        """Issue an email-verification token (default 24h)."""
        now = datetime.now(timezone.utc)
        payload = {
            "sub": subject,
            "type": VERIFY_EMAIL,
            "iss": self._issuer,
            "iat": now,
            "exp": now + timedelta(seconds=ttl_s),
        }
        return jwt.encode(payload, self._secret, algorithm=_ALGORITHM)

    def verify_email_token(self, token: str) -> str:
        """Validate an email-verification token and return the subject."""
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
        if payload.get("type") != VERIFY_EMAIL:
            raise TokenError("not an email-verification token")
        return payload["sub"]

    def password_reset_subject(self, token: str) -> str:
        """Return the subject of a reset token after validating signature/exp/type.

        Does not check the password-hash binding (the caller needs the subject
        first to look up the current hash); pair with verify_password_reset.
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
        if payload.get("type") != PASSWORD_RESET:
            raise TokenError("not a password-reset token")
        return payload["sub"]

    def verify_password_reset(self, token: str, current_password_hash: str) -> str:
        """Validate a reset token against the current hash; return the subject.

        Raises :class:`TokenError` if expired, tampered, wrong type, or already
        consumed (the bound password fingerprint no longer matches).
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
        if payload.get("type") != PASSWORD_RESET:
            raise TokenError("not a password-reset token")
        if payload.get("pwf") != _hash_fingerprint(current_password_hash):
            raise TokenError("reset token has already been used or is stale")
        return payload["sub"]

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
            jti=payload.get("jti", ""),
        )
