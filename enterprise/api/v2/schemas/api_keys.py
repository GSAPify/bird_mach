"""Pydantic schemas for api_keys."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class ApiKeysBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class ApiKeysCreate(ApiKeysBase):
        pass

    class ApiKeysUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class ApiKeysResponse(ApiKeysBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class ApiKeysList(BaseModel):
        items: list[ApiKeysResponse]
        total: int
        skip: int
        limit: int
