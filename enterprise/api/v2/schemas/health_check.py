"""Pydantic schemas for health_check."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class HealthCheckBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class HealthCheckCreate(HealthCheckBase):
        pass

    class HealthCheckUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class HealthCheckResponse(HealthCheckBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class HealthCheckList(BaseModel):
        items: list[HealthCheckResponse]
        total: int
        skip: int
        limit: int
