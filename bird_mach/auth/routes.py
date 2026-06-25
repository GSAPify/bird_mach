"""HTTP API for authentication and account management."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from bird_mach.auth.dependencies import get_auth_service, get_current_user
from bird_mach.auth.models import User
from bird_mach.auth.service import AuthService
from bird_mach.exceptions import (
    EmailAlreadyRegisteredError,
    InactiveUserError,
    InvalidCredentialsError,
    TokenError,
    UserNotFoundError,
)

router = APIRouter(prefix="/auth", tags=["auth"])


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


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest, service: AuthService = Depends(get_auth_service)) -> dict:
    try:
        user = service.register(body.email, body.password)
    except EmailAlreadyRegisteredError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered") from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc
    return user.public_dict()


@router.post("/login")
def login(body: LoginRequest, service: AuthService = Depends(get_auth_service)) -> dict:
    try:
        return service.login(body.email, body.password).as_dict()
    except InactiveUserError as exc:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is deactivated") from exc
    except InvalidCredentialsError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password") from exc


@router.post("/refresh")
def refresh(body: RefreshRequest, service: AuthService = Depends(get_auth_service)) -> dict:
    try:
        return service.refresh(body.refresh_token).as_dict()
    except (TokenError, UserNotFoundError, InactiveUserError) as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token") from exc


@router.get("/me")
def me(user: User = Depends(get_current_user)) -> dict:
    return user.public_dict()


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    body: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
) -> None:
    try:
        service.change_password(user.id, body.current_password, body.new_password)
    except InvalidCredentialsError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Current password is incorrect") from exc
    except ValueError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    user: User = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
) -> None:
    service.delete(user.id)
