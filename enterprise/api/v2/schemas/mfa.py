"""Pydantic schemas for mfa."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class MfaBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class MfaCreate(MfaBase):
        pass

    class MfaUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class MfaResponse(MfaBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class MfaList(BaseModel):
        items: list[MfaResponse]
        total: int
        skip: int
        limit: int
