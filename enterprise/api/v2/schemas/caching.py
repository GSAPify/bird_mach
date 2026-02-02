"""Pydantic schemas for caching."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class CachingBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class CachingCreate(CachingBase):
        pass

    class CachingUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class CachingResponse(CachingBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class CachingList(BaseModel):
        items: list[CachingResponse]
        total: int
        skip: int
        limit: int
