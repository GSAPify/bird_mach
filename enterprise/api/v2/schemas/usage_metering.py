"""Pydantic schemas for usage_metering."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class UsageMeteringBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class UsageMeteringCreate(UsageMeteringBase):
        pass

    class UsageMeteringUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class UsageMeteringResponse(UsageMeteringBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class UsageMeteringList(BaseModel):
        items: list[UsageMeteringResponse]
        total: int
        skip: int
        limit: int
