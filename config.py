"""Configuration management for YouTube automation."""
import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config(BaseModel):
    """Application configuration."""

    # API Keys
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    google_ai_api_key: str = Field(default_factory=lambda: os.getenv("GOOGLE_AI_API_KEY", ""))
    elevenlabs_api_key: str = Field(default_factory=lambda: os.getenv("ELEVENLABS_API_KEY", ""))

    # YouTube Credentials
    youtube_client_secrets: str = Field(
        default_factory=lambda: os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "client_secrets.json")
    )

    # Default Settings
    default_video_model: str = Field(default_factory=lambda: os.getenv("DEFAULT_VIDEO_MODEL", "veo"))
    default_language: str = Field(default_factory=lambda: os.getenv("DEFAULT_LANGUAGE", "en"))
    default_voice_id: Optional[str] = Field(default_factory=lambda: os.getenv("DEFAULT_VOICE_ID"))

    # Video Settings
    video_resolution: str = Field(default_factory=lambda: os.getenv("VIDEO_RESOLUTION", "1920x1080"))
    video_fps: int = Field(default_factory=lambda: int(os.getenv("VIDEO_FPS", "30")))
    max_video_duration: int = Field(default_factory=lambda: int(os.getenv("MAX_VIDEO_DURATION", "60")))

    # Directories
    output_dir: Path = Field(default_factory=lambda: Path(os.getenv("OUTPUT_DIR", "./output")))
    temp_dir: Path = Field(default_factory=lambda: Path(os.getenv("TEMP_DIR", "./temp")))

    def __init__(self, **data):
        super().__init__(**data)
        # Create directories if they don't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    @property
    def resolution_tuple(self) -> tuple[int, int]:
        """Parse resolution string to tuple."""
        width, height = self.video_resolution.split('x')
        return int(width), int(height)

    def validate_keys(self) -> dict[str, bool]:
        """Validate that required API keys are set."""
        return {
            "openai": bool(self.openai_api_key),
            "google_ai": bool(self.google_ai_api_key),
            "elevenlabs": bool(self.elevenlabs_api_key),
            "youtube": Path(self.youtube_client_secrets).exists()
        }


# Global config instance
config = Config()
