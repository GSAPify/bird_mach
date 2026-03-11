"""Pydantic schemas for alerting."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class AlertingBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class AlertingCreate(AlertingBase):
        pass

    class AlertingUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class AlertingResponse(AlertingBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class AlertingList(BaseModel):
        items: list[AlertingResponse]
        total: int
        skip: int
        limit: int
