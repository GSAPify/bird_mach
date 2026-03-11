"""Pydantic schemas for real_time."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class RealTimeBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class RealTimeCreate(RealTimeBase):
        pass

    class RealTimeUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class RealTimeResponse(RealTimeBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class RealTimeList(BaseModel):
        items: list[RealTimeResponse]
        total: int
        skip: int
        limit: int
