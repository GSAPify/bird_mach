"""Pydantic schemas for user_preferences."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class UserPreferencesBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class UserPreferencesCreate(UserPreferencesBase):
        pass

    class UserPreferencesUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class UserPreferencesResponse(UserPreferencesBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class UserPreferencesList(BaseModel):
        items: list[UserPreferencesResponse]
        total: int
        skip: int
        limit: int
