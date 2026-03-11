"""Pydantic schemas for pagination."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class PaginationBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class PaginationCreate(PaginationBase):
        pass

    class PaginationUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class PaginationResponse(PaginationBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class PaginationList(BaseModel):
        items: list[PaginationResponse]
        total: int
        skip: int
        limit: int
