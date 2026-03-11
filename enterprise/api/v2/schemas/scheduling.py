"""Pydantic schemas for scheduling."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class SchedulingBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class SchedulingCreate(SchedulingBase):
        pass

    class SchedulingUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class SchedulingResponse(SchedulingBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class SchedulingList(BaseModel):
        items: list[SchedulingResponse]
        total: int
        skip: int
        limit: int
