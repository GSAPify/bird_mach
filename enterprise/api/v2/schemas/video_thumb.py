"""Pydantic schemas for video_thumb."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class VideoThumbBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class VideoThumbCreate(VideoThumbBase):
        pass

    class VideoThumbUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class VideoThumbResponse(VideoThumbBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class VideoThumbList(BaseModel):
        items: list[VideoThumbResponse]
        total: int
        skip: int
        limit: int
