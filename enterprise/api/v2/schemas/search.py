"""Pydantic schemas for search."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class SearchBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class SearchCreate(SearchBase):
        pass

    class SearchUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class SearchResponse(SearchBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class SearchList(BaseModel):
        items: list[SearchResponse]
        total: int
        skip: int
        limit: int
