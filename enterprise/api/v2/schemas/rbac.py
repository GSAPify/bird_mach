"""Pydantic schemas for rbac."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class RbacBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class RbacCreate(RbacBase):
        pass

    class RbacUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class RbacResponse(RbacBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class RbacList(BaseModel):
        items: list[RbacResponse]
        total: int
        skip: int
        limit: int
