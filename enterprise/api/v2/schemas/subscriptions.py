"""Pydantic schemas for subscriptions."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class SubscriptionsBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class SubscriptionsCreate(SubscriptionsBase):
        pass

    class SubscriptionsUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class SubscriptionsResponse(SubscriptionsBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class SubscriptionsList(BaseModel):
        items: list[SubscriptionsResponse]
        total: int
        skip: int
        limit: int
