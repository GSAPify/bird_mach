"""Pydantic schemas for activity_feed."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class ActivityFeedBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class ActivityFeedCreate(ActivityFeedBase):
        pass

    class ActivityFeedUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class ActivityFeedResponse(ActivityFeedBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class ActivityFeedList(BaseModel):
        items: list[ActivityFeedResponse]
        total: int
        skip: int
        limit: int
