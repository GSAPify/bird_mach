"""Pydantic schemas for rate_limit."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class RateLimitBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class RateLimitCreate(RateLimitBase):
        pass

    class RateLimitUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class RateLimitResponse(RateLimitBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class RateLimitList(BaseModel):
        items: list[RateLimitResponse]
        total: int
        skip: int
        limit: int
