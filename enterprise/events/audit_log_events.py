"""audit_log domain events."""
from dataclasses import dataclass

@dataclass
class AuditLogCreated:
    id: str
    timestamp: float

@dataclass
class AuditLogUpdated:
    id: str
    changes: dict
