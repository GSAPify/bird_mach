"""Pydantic schemas for push."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class PushBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class PushCreate(PushBase):
        pass

    class PushUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class PushResponse(PushBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class PushList(BaseModel):
        items: list[PushResponse]
        total: int
        skip: int
        limit: int
