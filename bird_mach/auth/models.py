"""Domain models for user accounts and roles."""

from __future__ import annotations

import enum
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone


class Role(str, enum.Enum):
    """Coarse-grained authorization roles.

    Inherits from ``str`` so values serialise directly to JSON and compare
    equal to their string form, which keeps DB columns and API payloads plain.
    """

    USER = "user"
    ADMIN = "admin"


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class User:
    """A registered account.

    ``password_hash`` is never serialised by :meth:`public_dict`; callers that
    persist the user use :meth:`storage_dict` instead.
    """

    id: str
    email: str
    password_hash: str
    role: Role = Role.USER
    is_active: bool = True
    created_at: datetime = field(default_factory=_now)
    # Set when Stripe issues a customer for this user; links auth to billing
    # without the auth layer depending on the billing package.
    stripe_customer_id: str | None = None

    def public_dict(self) -> dict:
        """Safe-to-return representation: no secrets."""
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role.value,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "stripe_customer_id": self.stripe_customer_id,
        }

    def storage_dict(self) -> dict:
        d = asdict(self)
        d["role"] = self.role.value
        d["created_at"] = self.created_at.isoformat()
        return d
