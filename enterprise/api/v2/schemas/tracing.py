"""Pydantic schemas for tracing."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class TracingBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class TracingCreate(TracingBase):
        pass

    class TracingUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class TracingResponse(TracingBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class TracingList(BaseModel):
        items: list[TracingResponse]
        total: int
        skip: int
        limit: int
