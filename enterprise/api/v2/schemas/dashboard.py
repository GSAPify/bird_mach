"""Pydantic schemas for dashboard."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class DashboardBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class DashboardCreate(DashboardBase):
        pass

    class DashboardUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class DashboardResponse(DashboardBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class DashboardList(BaseModel):
        items: list[DashboardResponse]
        total: int
        skip: int
        limit: int
