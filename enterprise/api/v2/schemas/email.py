"""Pydantic schemas for email."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class EmailBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class EmailCreate(EmailBase):
        pass

    class EmailUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class EmailResponse(EmailBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class EmailList(BaseModel):
        items: list[EmailResponse]
        total: int
        skip: int
        limit: int
