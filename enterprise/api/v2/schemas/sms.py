"""Pydantic schemas for sms."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class SmsBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class SmsCreate(SmsBase):
        pass

    class SmsUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class SmsResponse(SmsBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class SmsList(BaseModel):
        items: list[SmsResponse]
        total: int
        skip: int
        limit: int
