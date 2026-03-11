"""Pydantic schemas for image_resize."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class ImageResizeBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class ImageResizeCreate(ImageResizeBase):
        pass

    class ImageResizeUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class ImageResizeResponse(ImageResizeBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class ImageResizeList(BaseModel):
        items: list[ImageResizeResponse]
        total: int
        skip: int
        limit: int
