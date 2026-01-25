"""Pydantic schemas for invoicing."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class InvoicingBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class InvoicingCreate(InvoicingBase):
        pass

    class InvoicingUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class InvoicingResponse(InvoicingBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class InvoicingList(BaseModel):
        items: list[InvoicingResponse]
        total: int
        skip: int
        limit: int
