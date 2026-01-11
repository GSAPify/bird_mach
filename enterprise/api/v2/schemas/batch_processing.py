"""Pydantic schemas for batch_processing."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class BatchProcessingBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class BatchProcessingCreate(BatchProcessingBase):
        pass

    class BatchProcessingUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class BatchProcessingResponse(BatchProcessingBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class BatchProcessingList(BaseModel):
        items: list[BatchProcessingResponse]
        total: int
        skip: int
        limit: int
