"""Pydantic schemas for logging."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class LoggingBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class LoggingCreate(LoggingBase):
        pass

    class LoggingUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class LoggingResponse(LoggingBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class LoggingList(BaseModel):
        items: list[LoggingResponse]
        total: int
        skip: int
        limit: int
