from pydantic import BaseModel, Field
from typing import Optional

class Video(BaseModel):
    video_id: str = Field(min_length=1, description="YouTube video ID")
    name: str = Field(min_length=1, description="Video title")
    description: Optional[str] = Field(default="", description="Video description")
    channel_name: str = Field(min_length=1, description="Channel name")
    channel_id: str = Field(min_length=1, description="Channel ID")
    duration: int = Field(ge=1, description="Video duration in seconds")
    video_transcript: str = Field(default="", description="Video transcript if available")
    thumbnail_url: Optional[str] = Field(default=None, description="Video thumbnail URL")
    published_at: Optional[str] = Field(default=None, description="Video publish date")
    view_count: int = Field(default=0, ge=0, description="Number of views")
    like_count: int = Field(default=0, ge=0, description="Number of likes")
    tags: list[str] = Field(default_factory=list, description="Video tags")