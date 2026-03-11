"""Pydantic schemas for sorting."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class SortingBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class SortingCreate(SortingBase):
        pass

    class SortingUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class SortingResponse(SortingBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class SortingList(BaseModel):
        items: list[SortingResponse]
        total: int
        skip: int
        limit: int
