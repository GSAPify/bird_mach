"""FastAPI wiring for authentication.

Builds a process-wide :class:`AuthService` from :class:`AppConfig` and exposes
dependencies for resolving the current user and gating routes by role. Kept
separate from :mod:`bird_mach.auth.routes` so the service can be reused by the
billing layer (which needs ``current_user``) without importing route handlers.
"""

from __future__ import annotations

import logging
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from bird_mach.auth.models import Role, User
from bird_mach.auth.service import AuthService
from bird_mach.auth.store import SqliteUserRepository, UserRepository
from bird_mach.auth.tokens import TokenService
from bird_mach.config import AppConfig
from bird_mach.db import Database
from bird_mach.exceptions import InactiveUserError, TokenError, UserNotFoundError

logger = logging.getLogger(__name__)

_bearer = HTTPBearer(auto_error=False)


def _resolve_secret(config: AppConfig) -> str:
    """Return the JWT secret, failing in production if it is unset.

    In non-production a random ephemeral secret is generated so local dev works
    out of the box; tokens simply don't survive a restart, which is fine there.
    """
    if config.jwt_secret:
        return config.jwt_secret
    if config.is_production:
        raise RuntimeError("JWT_SECRET must be set in production")
    logger.warning(
        "JWT_SECRET is unset; using an ephemeral dev secret. Tokens will not "
        "survive a restart. Set JWT_SECRET for stable sessions."
    )
    return secrets.token_urlsafe(48)


def build_auth_service(config: AppConfig, repo: UserRepository | None = None) -> AuthService:
    """Construct an AuthService from config. ``repo`` override is for tests."""
    if repo is None:
        repo = SqliteUserRepository(Database(config.auth_db_path))
    tokens = TokenService(
        _resolve_secret(config),
        access_ttl_s=config.access_token_ttl_s,
        refresh_ttl_s=config.refresh_token_ttl_s,
    )
    return AuthService(repo, tokens)


# Single shared instance for the running app. Tests build their own via
# build_auth_service() and override get_auth_service.
_service: AuthService | None = None


def get_auth_service() -> AuthService:
    global _service
    if _service is None:
        _service = build_auth_service(AppConfig.from_env())
    return _service


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    service: AuthService = Depends(get_auth_service),
) -> User:
    """Resolve the authenticated user from a Bearer access token."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        claims = service._tokens.verify(credentials.credentials)
        user = service._repo.get(claims.subject)
        if user is None:
            raise UserNotFoundError(claims.subject)
        if not user.is_active:
            raise InactiveUserError(user.id)
    except (TokenError, UserNotFoundError, InactiveUserError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    return user


def require_role(role: Role):
    """Dependency factory: 403 unless the current user has ``role``."""

    def _checker(user: User = Depends(get_current_user)) -> User:
        # Admins satisfy any role requirement.
        if user.role is not role and user.role is not Role.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {role.value} role",
            )
        return user

    return _checker
