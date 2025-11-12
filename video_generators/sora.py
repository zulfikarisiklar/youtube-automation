"""OpenAI Sora video generator."""
import asyncio
import time
from pathlib import Path
from typing import Optional
import requests
from openai import OpenAI

from .base import VideoGenerator


class SoraGenerator(VideoGenerator):
    """OpenAI Sora video generator."""

    def __init__(self, api_key: str):
        """Initialize Sora generator.

        Args:
            api_key: OpenAI API key
        """
        super().__init__(api_key)
        self.client = OpenAI(api_key=api_key)

    def get_model_name(self) -> str:
        """Get the model name."""
        return "sora"

    async def generate(
        self,
        prompt: str,
        duration: int = 5,
        resolution: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        output_path: Optional[Path] = None
    ) -> Path:
        """Generate video using Sora.

        Args:
            prompt: Text prompt for video generation
            duration: Video duration in seconds
            resolution: Video resolution (e.g., "1920x1080")
            aspect_ratio: Aspect ratio (e.g., "16:9")
            output_path: Path to save the generated video

        Returns:
            Path to the generated video file
        """
        if output_path is None:
            output_path = Path(f"sora_video_{int(time.time())}.mp4")

        print(f"Generating video with Sora: {prompt}")
        print(f"Duration: {duration}s")

        # Note: As of this implementation, Sora API might not be publicly available
        # This is a placeholder implementation that shows the expected structure
        try:
            # Prepare generation parameters
            params = {
                "prompt": prompt,
                "duration": duration
            }

            if resolution:
                params["resolution"] = resolution
            if aspect_ratio:
                params["aspect_ratio"] = aspect_ratio

            # Call Sora API (placeholder - adjust based on actual API)
            # The actual implementation will depend on OpenAI's final Sora API structure
            response = await asyncio.to_thread(
                self._generate_sync,
                params
            )

            # Download the video
            video_data = response.get("video_data")
            if video_data:
                output_path.write_bytes(video_data)
            else:
                video_url = response.get("video_url")
                if video_url:
                    video_response = requests.get(video_url)
                    video_response.raise_for_status()
                    output_path.write_bytes(video_response.content)

            print(f"Video generated successfully: {output_path}")
            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to generate video with Sora: {str(e)}")

    def _generate_sync(self, params: dict) -> dict:
        """Synchronous video generation call.

        Args:
            params: Generation parameters

        Returns:
            Response dictionary with video data or URL
        """
        # Placeholder for actual Sora API call
        # When Sora API is available, replace this with actual implementation

        # Example structure (adjust based on actual API):
        # response = self.client.videos.generate(**params)
        # return {"video_url": response.url}

        raise NotImplementedError(
            "Sora API is not yet publicly available. "
            "Please update this implementation when the API is released. "
            "For now, please use the 'veo' model instead."
        )
