"""Pydantic schemas for report_generation."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class ReportGenerationBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class ReportGenerationCreate(ReportGenerationBase):
        pass

    class ReportGenerationUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class ReportGenerationResponse(ReportGenerationBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class ReportGenerationList(BaseModel):
        items: list[ReportGenerationResponse]
        total: int
        skip: int
        limit: int
