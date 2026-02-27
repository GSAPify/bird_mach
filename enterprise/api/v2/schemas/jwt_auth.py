"""Pydantic schemas for jwt_auth."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class JwtAuthBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class JwtAuthCreate(JwtAuthBase):
        pass

    class JwtAuthUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class JwtAuthResponse(JwtAuthBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class JwtAuthList(BaseModel):
        items: list[JwtAuthResponse]
        total: int
        skip: int
        limit: int
