"""Authentication service: the orchestration layer over the repository.

This is the only place that combines password hashing, token minting, and the
user repository. Routes and FastAPI dependencies call into here; they never
touch hashing or SQL directly.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass

from bird_mach.auth.models import Role, User
from bird_mach.auth.passwords import hash_password, needs_rehash, verify_password
from bird_mach.auth.store import UserRepository
from bird_mach.auth.tokens import REFRESH_TOKEN, TokenService
from bird_mach.exceptions import (
    EmailAlreadyRegisteredError,
    InactiveUserError,
    InvalidCredentialsError,
    UserNotFoundError,
)

# Pragmatic email shape check — full RFC 5322 validation is famously not worth
# it; deliverability is proven by sending mail, not by a regex.
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_MIN_PASSWORD_LEN = 8


@dataclass(frozen=True)
class TokenPair:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    def as_dict(self) -> dict:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "token_type": self.token_type,
        }


def _validate_email(email: str) -> str:
    email = email.strip().lower()
    if not _EMAIL_RE.match(email):
        raise ValueError(f"invalid email address: {email!r}")
    return email


def _validate_password(password: str) -> None:
    if len(password) < _MIN_PASSWORD_LEN:
        raise ValueError(f"password must be at least {_MIN_PASSWORD_LEN} characters")


class AuthService:
    def __init__(self, repo: UserRepository, tokens: TokenService) -> None:
        self._repo = repo
        self._tokens = tokens

    def register(self, email: str, password: str, *, role: Role = Role.USER) -> User:
        email = _validate_email(email)
        _validate_password(password)
        if self._repo.get_by_email(email) is not None:
            raise EmailAlreadyRegisteredError(email)
        user = User(
            id=uuid.uuid4().hex,
            email=email,
            password_hash=hash_password(password),
            role=role,
        )
        return self._repo.add(user)

    def authenticate(self, email: str, password: str) -> User:
        """Return the user for valid credentials, else raise.

        The same :class:`InvalidCredentialsError` is raised whether the email
        is unknown or the password is wrong, so the response cannot be used to
        enumerate which emails are registered.
        """
        user = self._repo.get_by_email(email.strip().lower())
        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("invalid email or password")
        if not user.is_active:
            raise InactiveUserError(user.id)
        # Transparently upgrade the stored hash if the cost factor has risen.
        if needs_rehash(user.password_hash):
            user.password_hash = hash_password(password)
            self._repo.update(user)
        return user

    def login(self, email: str, password: str) -> TokenPair:
        user = self.authenticate(email, password)
        return self._issue_pair(user)

    def refresh(self, refresh_token: str) -> TokenPair:
        claims = self._tokens.verify(refresh_token, expected_type=REFRESH_TOKEN)
        user = self._repo.get(claims.subject)
        if user is None:
            raise UserNotFoundError(claims.subject)
        if not user.is_active:
            raise InactiveUserError(user.id)
        return self._issue_pair(user)

    def request_password_reset(self, email: str) -> str | None:
        """Issue a reset token for an active account, else None.

        Returns None for unknown/inactive accounts so the caller can respond
        identically regardless of whether the email exists (no enumeration).
        """
        user = self._repo.get_by_email(email.strip().lower())
        if user is None or not user.is_active:
            return None
        return self._tokens.issue_password_reset(user.id, user.password_hash)

    def reset_password(self, token: str, new_password: str) -> None:
        """Consume a reset token and set a new password."""
        subject = self._tokens.password_reset_subject(token)
        user = self._repo.get(subject)
        if user is None:
            raise UserNotFoundError(subject)
        # Binds the token to the current hash → using it invalidates the token.
        self._tokens.verify_password_reset(token, user.password_hash)
        _validate_password(new_password)
        user.password_hash = hash_password(new_password)
        self._repo.update(user)

    def issue_email_verification(self, user_id: str) -> str:
        """Issue an email-verification token for an existing user."""
        user = self._require_user(user_id)
        return self._tokens.issue_email_verification(user.id)

    def verify_email(self, token: str) -> User:
        """Consume a verification token and mark the account verified."""
        subject = self._tokens.verify_email_token(token)
        user = self._repo.get(subject)
        if user is None:
            raise UserNotFoundError(subject)
        if not user.is_verified:
            user.is_verified = True
            self._repo.update(user)
        return user

    def change_password(self, user_id: str, current: str, new: str) -> None:
        user = self._require_user(user_id)
        if not verify_password(current, user.password_hash):
            raise InvalidCredentialsError("current password is incorrect")
        _validate_password(new)
        user.password_hash = hash_password(new)
        self._repo.update(user)

    def deactivate(self, user_id: str) -> User:
        user = self._require_user(user_id)
        user.is_active = False
        return self._repo.update(user)

    def reactivate(self, user_id: str) -> User:
        user = self._require_user(user_id)
        user.is_active = True
        return self._repo.update(user)

    def set_role(self, user_id: str, role: Role) -> User:
        user = self._require_user(user_id)
        user.role = role
        return self._repo.update(user)

    def list_users(self, *, limit: int = 100, offset: int = 0) -> list[User]:
        return self._repo.list_all(limit=limit, offset=offset)

    def get_user(self, user_id: str) -> User:
        return self._require_user(user_id)

    def delete(self, user_id: str) -> None:
        if not self._repo.delete(user_id):
            raise UserNotFoundError(user_id)

    def _issue_pair(self, user: User) -> TokenPair:
        return TokenPair(
            access_token=self._tokens.issue_access(user.id, user.role.value),
            refresh_token=self._tokens.issue_refresh(user.id, user.role.value),
        )

    def _require_user(self, user_id: str) -> User:
        user = self._repo.get(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user
