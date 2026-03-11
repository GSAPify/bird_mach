"""Pydantic schemas for data_export."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class DataExportBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class DataExportCreate(DataExportBase):
        pass

    class DataExportUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class DataExportResponse(DataExportBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class DataExportList(BaseModel):
        items: list[DataExportResponse]
        total: int
        skip: int
        limit: int
