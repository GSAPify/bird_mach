"""Pydantic schemas for team_mgmt."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class TeamMgmtBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class TeamMgmtCreate(TeamMgmtBase):
        pass

    class TeamMgmtUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class TeamMgmtResponse(TeamMgmtBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class TeamMgmtList(BaseModel):
        items: list[TeamMgmtResponse]
        total: int
        skip: int
        limit: int
