"""Pydantic schemas for metrics."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class MetricsBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class MetricsCreate(MetricsBase):
        pass

    class MetricsUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class MetricsResponse(MetricsBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class MetricsList(BaseModel):
        items: list[MetricsResponse]
        total: int
        skip: int
        limit: int
