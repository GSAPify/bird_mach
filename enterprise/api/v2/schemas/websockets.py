"""Pydantic schemas for websockets."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class WebsocketsBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class WebsocketsCreate(WebsocketsBase):
        pass

    class WebsocketsUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class WebsocketsResponse(WebsocketsBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class WebsocketsList(BaseModel):
        items: list[WebsocketsResponse]
        total: int
        skip: int
        limit: int
