"""Pydantic schemas for webhooks."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class WebhooksBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class WebhooksCreate(WebhooksBase):
        pass

    class WebhooksUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class WebhooksResponse(WebhooksBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class WebhooksList(BaseModel):
        items: list[WebhooksResponse]
        total: int
        skip: int
        limit: int
