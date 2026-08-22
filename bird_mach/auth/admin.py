"""Admin-only user management API.

Every route requires the ADMIN role (enforced via require_role). These let an
operator enumerate accounts, inspect one, deactivate/reactivate, and change a
user's role.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from bird_mach.auth.dependencies import get_auth_service, get_current_user, require_role
from bird_mach.auth.models import Role, User
from bird_mach.auth.service import AuthService
from bird_mach.exceptions import UserNotFoundError

# Gate the whole router: only admins reach any handler here.
router = APIRouter(
    prefix="/auth/admin",
    tags=["admin"],
    dependencies=[Depends(require_role(Role.ADMIN))],
)


class RoleUpdate(BaseModel):
    role: Role


@router.get("/users")
def list_users(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    service: AuthService = Depends(get_auth_service),
) -> dict:
    users = service.list_users(limit=limit, offset=offset)
    return {"users": [u.public_dict() for u in users], "limit": limit, "offset": offset}


@router.get("/users/{user_id}")
def get_user(user_id: str, service: AuthService = Depends(get_auth_service)) -> dict:
    try:
        return service.get_user(user_id).public_dict()
    except UserNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found") from exc


@router.post("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: str,
    current: User = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
) -> dict:
    if user_id == current.id:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Cannot deactivate your own account"
        )
    try:
        return service.deactivate(user_id).public_dict()
    except UserNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found") from exc


@router.post("/users/{user_id}/activate")
def activate_user(user_id: str, service: AuthService = Depends(get_auth_service)) -> dict:
    try:
        return service.reactivate(user_id).public_dict()
    except UserNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found") from exc


@router.put("/users/{user_id}/role")
def set_user_role(
    user_id: str,
    body: RoleUpdate,
    current: User = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
) -> dict:
    if user_id == current.id and body.role is not Role.ADMIN:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Cannot demote your own admin role"
        )
    try:
        return service.set_role(user_id, body.role).public_dict()
    except UserNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found") from exc
