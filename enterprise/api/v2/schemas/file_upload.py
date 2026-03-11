"""Pydantic schemas for file_upload."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class FileUploadBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class FileUploadCreate(FileUploadBase):
        pass

    class FileUploadUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class FileUploadResponse(FileUploadBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class FileUploadList(BaseModel):
        items: list[FileUploadResponse]
        total: int
        skip: int
        limit: int
