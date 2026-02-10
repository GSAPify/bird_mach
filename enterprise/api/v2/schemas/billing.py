"""Pydantic schemas for billing."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class BillingBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class BillingCreate(BillingBase):
        pass

    class BillingUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class BillingResponse(BillingBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class BillingList(BaseModel):
        items: list[BillingResponse]
        total: int
        skip: int
        limit: int
