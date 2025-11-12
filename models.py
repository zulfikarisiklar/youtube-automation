"""Data models for video generation."""
from typing import Optional, Literal
from pydantic import BaseModel, Field


class VideoRequest(BaseModel):
    """Request for video generation."""

    prompt: str = Field(..., description="Text prompt for video generation")
    model: Literal["veo", "sora"] = Field(default="veo", description="Video generation model")
    duration: int = Field(default=5, ge=1, le=60, description="Video duration in seconds")
    resolution: Optional[str] = Field(default=None, description="Video resolution (e.g., 1920x1080)")
    aspect_ratio: Optional[str] = Field(default=None, description="Aspect ratio (e.g., 16:9)")


class AudioRequest(BaseModel):
    """Request for audio generation."""

    text: str = Field(..., description="Text to convert to speech")
    language: str = Field(default="en", description="Language code (e.g., en, es, fr)")
    voice_id: Optional[str] = Field(default=None, description="ElevenLabs voice ID")
    model_id: str = Field(default="eleven_multilingual_v2", description="ElevenLabs model ID")


class YouTubeMetadata(BaseModel):
    """Metadata for YouTube upload."""

    title: str = Field(..., description="Video title")
    description: str = Field(default="", description="Video description")
    tags: list[str] = Field(default_factory=list, description="Video tags")
    category_id: str = Field(default="22", description="YouTube category ID (22 = People & Blogs)")
    privacy_status: Literal["public", "private", "unlisted"] = Field(
        default="private",
        description="Video privacy status"
    )
    language: str = Field(default="en", description="Video language")


class VideoProject(BaseModel):
    """Complete video project configuration."""

    video_request: VideoRequest
    audio_request: Optional[AudioRequest] = None
    youtube_metadata: YouTubeMetadata
    output_filename: Optional[str] = None
