"""Pydantic schemas for project_mgmt."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class ProjectMgmtBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class ProjectMgmtCreate(ProjectMgmtBase):
        pass

    class ProjectMgmtUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class ProjectMgmtResponse(ProjectMgmtBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class ProjectMgmtList(BaseModel):
        items: list[ProjectMgmtResponse]
        total: int
        skip: int
        limit: int
