"""Pydantic schemas for oauth2."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class Oauth2Base(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class Oauth2Create(Oauth2Base):
        pass

    class Oauth2Update(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class Oauth2Response(Oauth2Base):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class Oauth2List(BaseModel):
        items: list[Oauth2Response]
        total: int
        skip: int
        limit: int
