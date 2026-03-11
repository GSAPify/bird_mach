"""Pydantic schemas for sse."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class SseBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class SseCreate(SseBase):
        pass

    class SseUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class SseResponse(SseBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class SseList(BaseModel):
        items: list[SseResponse]
        total: int
        skip: int
        limit: int
