"""Pydantic schemas for task_queue."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class TaskQueueBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class TaskQueueCreate(TaskQueueBase):
        pass

    class TaskQueueUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class TaskQueueResponse(TaskQueueBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class TaskQueueList(BaseModel):
        items: list[TaskQueueResponse]
        total: int
        skip: int
        limit: int
