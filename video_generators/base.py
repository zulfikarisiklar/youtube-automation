"""Base class for video generators."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class VideoGenerator(ABC):
    """Abstract base class for video generators."""

    def __init__(self, api_key: str):
        """Initialize video generator.

        Args:
            api_key: API key for the video generation service
        """
        self.api_key = api_key

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        duration: int = 5,
        resolution: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        output_path: Optional[Path] = None
    ) -> Path:
        """Generate video from prompt.

        Args:
            prompt: Text prompt for video generation
            duration: Video duration in seconds
            resolution: Video resolution (e.g., "1920x1080")
            aspect_ratio: Aspect ratio (e.g., "16:9")
            output_path: Path to save the generated video

        Returns:
            Path to the generated video file
        """
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Get the model name."""
        pass
