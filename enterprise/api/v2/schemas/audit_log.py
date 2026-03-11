"""Pydantic schemas for audit_log."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class AuditLogBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class AuditLogCreate(AuditLogBase):
        pass

    class AuditLogUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class AuditLogResponse(AuditLogBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class AuditLogList(BaseModel):
        items: list[AuditLogResponse]
        total: int
        skip: int
        limit: int
