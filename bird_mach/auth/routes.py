"""HTTP API for authentication and account management."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from bird_mach.auth.audit import AuditLog, AuthEvent, AuthEventType
from bird_mach.auth.dependencies import get_audit_log, get_auth_service, get_current_user
from bird_mach.auth.models import User
from bird_mach.auth.ratelimit import login_rate_limit
from bird_mach.auth.service import AuthService
from bird_mach.config import AppConfig
from bird_mach.exceptions import (
    EmailAlreadyRegisteredError,
    InactiveUserError,
    InvalidCredentialsError,
    TokenError,
    UserNotFoundError,
)

logger = logging.getLogger(__name__)
config = AppConfig.from_env()

router = APIRouter(prefix="/auth", tags=["auth"])


def _ip(request: Request) -> str | None:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else None


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class VerifyEmailConfirm(BaseModel):
    token: str


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(login_rate_limit)],
)
def register(
    body: RegisterRequest,
    request: Request,
    service: AuthService = Depends(get_auth_service),
    audit: AuditLog = Depends(get_audit_log),
) -> dict:
    try:
        user = service.register(body.email, body.password)
    except EmailAlreadyRegisteredError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered") from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc
    audit.record(
        AuthEvent(AuthEventType.REGISTERED, user_id=user.id, email=user.email, ip=_ip(request))
    )
    return user.public_dict()


@router.post("/login", dependencies=[Depends(login_rate_limit)])
def login(
    body: LoginRequest,
    request: Request,
    service: AuthService = Depends(get_auth_service),
    audit: AuditLog = Depends(get_audit_log),
) -> dict:
    try:
        user = service.authenticate(body.email, body.password)
    except InactiveUserError as exc:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is deactivated") from exc
    except InvalidCredentialsError as exc:
        audit.record(
            AuthEvent(AuthEventType.LOGIN_FAILURE, email=body.email, ip=_ip(request))
        )
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password") from exc
    audit.record(
        AuthEvent(AuthEventType.LOGIN_SUCCESS, user_id=user.id, email=user.email, ip=_ip(request))
    )
    return service._issue_pair(user).as_dict()


@router.post("/refresh")
def refresh(body: RefreshRequest, service: AuthService = Depends(get_auth_service)) -> dict:
    try:
        return service.refresh(body.refresh_token).as_dict()
    except (TokenError, UserNotFoundError, InactiveUserError) as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token") from exc


@router.post(
    "/password-reset/request",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(login_rate_limit)],
)
def request_password_reset(
    body: PasswordResetRequest,
    service: AuthService = Depends(get_auth_service),
) -> dict:
    """Begin a password reset. Always 202, regardless of whether the email exists.

    In production the token would be emailed to the user. There is no email
    provider wired here, so the token is logged and (in non-production only)
    returned in the response for local testing.
    """
    token = service.request_password_reset(body.email)
    if token is not None:
        logger.info("password reset requested for %s", body.email)
    response: dict = {"status": "accepted"}
    if token is not None and not config.is_production:
        response["debug_reset_token"] = token
    return response


@router.post("/password-reset/confirm", status_code=status.HTTP_204_NO_CONTENT)
def confirm_password_reset(
    body: PasswordResetConfirm,
    service: AuthService = Depends(get_auth_service),
) -> None:
    try:
        service.reset_password(body.token, body.new_password)
    except (TokenError, UserNotFoundError) as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired reset token") from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc


@router.post("/verify-email/request", status_code=status.HTTP_202_ACCEPTED)
def request_email_verification(
    user: User = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
) -> dict:
    """Issue an email-verification token for the current user.

    Production emails the link; with no email provider wired, the token is
    logged and returned in non-production for local testing.
    """
    if user.is_verified:
        return {"status": "already_verified"}
    token = service.issue_email_verification(user.id)
    logger.info("email verification requested for %s", user.email)
    response: dict = {"status": "accepted"}
    if not config.is_production:
        response["debug_verification_token"] = token
    return response


@router.post("/verify-email/confirm")
def confirm_email_verification(
    body: VerifyEmailConfirm,
    service: AuthService = Depends(get_auth_service),
) -> dict:
    try:
        user = service.verify_email(body.token)
    except (TokenError, UserNotFoundError) as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired token") from exc
    return {"status": "verified", "email": user.email, "is_verified": user.is_verified}


@router.get("/me")
def me(user: User = Depends(get_current_user)) -> dict:
    return user.public_dict()


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    body: ChangePasswordRequest,
    request: Request,
    user: User = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
    audit: AuditLog = Depends(get_audit_log),
) -> None:
    try:
        service.change_password(user.id, body.current_password, body.new_password)
    except InvalidCredentialsError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Current password is incorrect") from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc
    audit.record(
        AuthEvent(
            AuthEventType.PASSWORD_CHANGED, user_id=user.id, email=user.email, ip=_ip(request)
        )
    )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    request: Request,
    user: User = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
    audit: AuditLog = Depends(get_audit_log),
) -> None:
    service.delete(user.id)
    audit.record(
        AuthEvent(
            AuthEventType.ACCOUNT_DELETED, user_id=user.id, email=user.email, ip=_ip(request)
        )
    )


@router.get("/events")
def my_events(
    user: User = Depends(get_current_user),
    audit: AuditLog = Depends(get_audit_log),
) -> dict:
    """Return the current user's recent security events."""
    return {"events": [e.public_dict() for e in audit.recent_for_user(user.id)]}
