"""Fine-grained permissions for collaboration."""
from __future__ import annotations
from enum import Flag, auto

class Permission(Flag):
    VIEW = auto()
    ANNOTATE = auto()
    COMMENT = auto()
    EDIT = auto()
    ADMIN = auto()
    ALL = VIEW | ANNOTATE | COMMENT | EDIT | ADMIN

ROLE_PERMISSIONS = {
    "viewer": Permission.VIEW,
    "commenter": Permission.VIEW | Permission.COMMENT,
    "annotator": Permission.VIEW | Permission.ANNOTATE | Permission.COMMENT,
    "editor": Permission.VIEW | Permission.ANNOTATE | Permission.COMMENT | Permission.EDIT,
    "admin": Permission.ALL,
}

def has_permission(role: str, required: Permission) -> bool:
    perms = ROLE_PERMISSIONS.get(role, Permission(0))
    return required in perms
