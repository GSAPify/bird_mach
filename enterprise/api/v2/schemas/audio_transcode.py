"""Pydantic schemas for audio_transcode."""
    from pydantic import BaseModel, Field
    from datetime import datetime
    from typing import Optional

    class AudioTranscodeBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=255)
        description: Optional[str] = None
        enabled: bool = True

    class AudioTranscodeCreate(AudioTranscodeBase):
        pass

    class AudioTranscodeUpdate(BaseModel):
        name: Optional[str] = None
        description: Optional[str] = None
        enabled: Optional[bool] = None

    class AudioTranscodeResponse(AudioTranscodeBase):
        id: str
        created_at: datetime
        updated_at: datetime
        class Config:
            from_attributes = True

    class AudioTranscodeList(BaseModel):
        items: list[AudioTranscodeResponse]
        total: int
        skip: int
        limit: int
