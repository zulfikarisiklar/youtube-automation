"""Main video automation orchestrator."""
from pathlib import Path
from typing import Optional

from config import config
from models import VideoRequest, AudioRequest, YouTubeMetadata, VideoProject
from video_generators import SoraGenerator, VeoGenerator
from audio_generator import AudioGenerator
from video_processor import VideoProcessor
from youtube_uploader import YouTubeUploader


class VideoAutomation:
    """Main orchestrator for automated video generation and upload."""

    def __init__(self):
        """Initialize video automation system."""
        self.config = config
        self.video_generator = None
        self.audio_generator = None
        self.video_processor = VideoProcessor()
        self.youtube_uploader = None

    def initialize(self, video_model: str = "veo") -> None:
        """Initialize generators based on configuration.

        Args:
            video_model: Video generation model to use ("veo" or "sora")
        """
        print("Initializing video automation system...")

        # Validate API keys
        keys_status = self.config.validate_keys()
        print(f"API Keys Status: {keys_status}")

        # Initialize video generator
        if video_model == "sora":
            if not keys_status["openai"]:
                raise ValueError("OpenAI API key not configured")
            self.video_generator = SoraGenerator(self.config.openai_api_key)
        elif video_model == "veo":
            if not keys_status["google_ai"]:
                raise ValueError("Google AI API key not configured")
            self.video_generator = VeoGenerator(self.config.google_ai_api_key)
        else:
            raise ValueError(f"Unknown video model: {video_model}")

        # Initialize audio generator
        if keys_status["elevenlabs"]:
            self.audio_generator = AudioGenerator(self.config.elevenlabs_api_key)
        else:
            print("Warning: ElevenLabs API key not configured. Audio generation will be disabled.")

        # Initialize YouTube uploader
        if keys_status["youtube"]:
            self.youtube_uploader = YouTubeUploader(self.config.youtube_client_secrets)
        else:
            print("Warning: YouTube credentials not configured. Upload will be disabled.")

        print(f"Initialization complete! Using {video_model} for video generation.")

    async def create_video(
        self,
        video_request: VideoRequest,
        audio_request: Optional[AudioRequest] = None,
        output_path: Optional[Path] = None
    ) -> Path:
        """Create a video with optional audio.

        Args:
            video_request: Video generation request
            audio_request: Audio generation request (optional)
            output_path: Path to save the final video

        Returns:
            Path to the created video
        """
        if not self.video_generator:
            raise RuntimeError("Video generator not initialized. Call initialize() first.")

        print("\n" + "="*60)
        print("STARTING VIDEO CREATION")
        print("="*60)

        # Generate video
        print("\n[1/3] Generating video...")
        video_path = await self.video_generator.generate(
            prompt=video_request.prompt,
            duration=video_request.duration,
            resolution=video_request.resolution,
            aspect_ratio=video_request.aspect_ratio,
            output_path=self.config.temp_dir / "generated_video.mp4"
        )

        # Generate audio if requested
        if audio_request and self.audio_generator:
            print("\n[2/3] Generating audio...")
            audio_path = await self.audio_generator.generate(
                text=audio_request.text,
                language=audio_request.language,
                voice_id=audio_request.voice_id,
                model_id=audio_request.model_id,
                output_path=self.config.temp_dir / "generated_audio.mp3"
            )

            # Merge video and audio
            print("\n[3/3] Merging video and audio...")
            if output_path is None:
                output_path = self.config.output_dir / "final_video.mp4"

            final_path = await self.video_processor.merge_audio_video(
                video_path=video_path,
                audio_path=audio_path,
                output_path=output_path
            )
        else:
            print("\n[2/3] Skipping audio generation...")
            print("[3/3] Using video without audio...")
            final_path = video_path

        print("\n" + "="*60)
        print(f"VIDEO CREATION COMPLETE: {final_path}")
        print("="*60 + "\n")

        return final_path

    async def create_and_upload(
        self,
        video_request: VideoRequest,
        youtube_metadata: YouTubeMetadata,
        audio_request: Optional[AudioRequest] = None,
        authenticate: bool = True
    ) -> dict:
        """Create video and upload to YouTube.

        Args:
            video_request: Video generation request
            youtube_metadata: YouTube video metadata
            audio_request: Audio generation request (optional)
            authenticate: Whether to authenticate with YouTube

        Returns:
            Dictionary with upload information
        """
        if not self.youtube_uploader:
            raise RuntimeError("YouTube uploader not initialized")

        # Authenticate with YouTube
        if authenticate:
            self.youtube_uploader.authenticate()

        # Create video
        video_path = await self.create_video(
            video_request=video_request,
            audio_request=audio_request
        )

        # Upload to YouTube
        print("\n" + "="*60)
        print("UPLOADING TO YOUTUBE")
        print("="*60 + "\n")

        upload_info = await self.youtube_uploader.upload(
            video_path=video_path,
            metadata=youtube_metadata
        )

        print("\n" + "="*60)
        print("UPLOAD COMPLETE")
        print(f"Video URL: {upload_info['url']}")
        print("="*60 + "\n")

        return upload_info

    async def batch_create(
        self,
        projects: list[VideoProject],
        upload: bool = False
    ) -> list[dict]:
        """Create multiple videos in batch.

        Args:
            projects: List of video projects
            upload: Whether to upload videos to YouTube

        Returns:
            List of results (paths or upload info)
        """
        results = []

        for i, project in enumerate(projects, 1):
            print(f"\n{'='*60}")
            print(f"PROCESSING PROJECT {i}/{len(projects)}")
            print(f"{'='*60}\n")

            try:
                if upload:
                    result = await self.create_and_upload(
                        video_request=project.video_request,
                        youtube_metadata=project.youtube_metadata,
                        audio_request=project.audio_request,
                        authenticate=(i == 1)  # Only authenticate once
                    )
                else:
                    output_path = None
                    if project.output_filename:
                        output_path = self.config.output_dir / project.output_filename

                    result = await self.create_video(
                        video_request=project.video_request,
                        audio_request=project.audio_request,
                        output_path=output_path
                    )

                results.append({
                    "success": True,
                    "project_index": i,
                    "result": result
                })

            except Exception as e:
                print(f"\nError processing project {i}: {str(e)}\n")
                results.append({
                    "success": False,
                    "project_index": i,
                    "error": str(e)
                })

        # Summary
        successful = sum(1 for r in results if r["success"])
        print("\n" + "="*60)
        print("BATCH PROCESSING COMPLETE")
        print(f"Successful: {successful}/{len(projects)}")
        print("="*60 + "\n")

        return results

    def list_available_voices(self) -> list[dict]:
        """List available ElevenLabs voices.

        Returns:
            List of available voices
        """
        if not self.audio_generator:
            raise RuntimeError("Audio generator not initialized")

        return self.audio_generator.list_voices()

    def get_supported_languages(self) -> list[str]:
        """Get list of supported languages.

        Returns:
            List of language codes
        """
        if not self.audio_generator:
            raise RuntimeError("Audio generator not initialized")

        return self.audio_generator.SUPPORTED_LANGUAGES
