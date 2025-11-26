#!/usr/bin/env python3
"""Simple example of using the video automation API."""
import asyncio
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from video_automation import VideoAutomation
from models import VideoRequest, AudioRequest, YouTubeMetadata


async def create_simple_video():
    """Create a simple video with audio."""
    print("Creating a simple video with audio...")

    # Initialize automation
    automation = VideoAutomation()
    automation.initialize(video_model="veo")

    # Create video request
    video_request = VideoRequest(
        prompt="A cute cat playing with a ball of yarn",
        model="veo",
        duration=5
    )

    # Create audio request
    audio_request = AudioRequest(
        text="Look at this adorable cat playing with yarn!",
        language="en"
    )

    # Generate video
    video_path = await automation.create_video(
        video_request=video_request,
        audio_request=audio_request,
        output_path=Path("output/cute_cat.mp4")
    )

    print(f"\nVideo created successfully: {video_path}")


async def create_and_upload():
    """Create a video and upload to YouTube."""
    print("Creating and uploading video to YouTube...")

    # Initialize automation
    automation = VideoAutomation()
    automation.initialize(video_model="veo")

    # Create video request
    video_request = VideoRequest(
        prompt="A peaceful waterfall in a lush green forest",
        model="veo",
        duration=5
    )

    # Create audio request
    audio_request = AudioRequest(
        text="Experience the serenity of nature with this peaceful waterfall",
        language="en"
    )

    # Create YouTube metadata
    youtube_metadata = YouTubeMetadata(
        title="Peaceful Waterfall - Nature Sounds",
        description="An AI-generated video of a peaceful waterfall in a lush forest. Perfect for relaxation and meditation.",
        tags=["waterfall", "nature", "relaxation", "peaceful", "ai"],
        privacy_status="private",
        category_id="22"
    )

    # Create and upload
    result = await automation.create_and_upload(
        video_request=video_request,
        youtube_metadata=youtube_metadata,
        audio_request=audio_request
    )

    print("\nVideo uploaded successfully!")
    print(f"Video URL: {result['url']}")
    print(f"Video ID: {result['id']}")


async def create_multilingual_video():
    """Create videos in different languages."""
    print("Creating videos in multiple languages...")

    automation = VideoAutomation()
    automation.initialize(video_model="veo")

    # Languages to create videos in
    languages = {
        "en": "Welcome to our channel! Enjoy this amazing video.",
        "es": "¡Bienvenido a nuestro canal! Disfruta de este increíble video.",
        "fr": "Bienvenue sur notre chaîne ! Profitez de cette vidéo incroyable.",
        "de": "Willkommen auf unserem Kanal! Genießen Sie dieses erstaunliche Video."
    }

    for lang_code, text in languages.items():
        print(f"\nCreating video in {lang_code}...")

        video_request = VideoRequest(
            prompt="A beautiful landscape with mountains and valleys",
            model="veo",
            duration=5
        )

        audio_request = AudioRequest(
            text=text,
            language=lang_code
        )

        video_path = await automation.create_video(
            video_request=video_request,
            audio_request=audio_request,
            output_path=Path(f"output/landscape_{lang_code}.mp4")
        )

        print(f"Created: {video_path}")


async def list_available_voices():
    """List all available ElevenLabs voices."""
    print("Listing available voices...")

    automation = VideoAutomation()
    automation.initialize()

    voices = automation.list_available_voices()

    print(f"\nFound {len(voices)} voices:")
    print("-" * 60)
    for voice in voices[:10]:  # Show first 10
        print(f"Name: {voice['name']}")
        print(f"ID: {voice['voice_id']}")
        print(f"Category: {voice['category']}")
        print()


async def main():
    """Main function to run examples."""
    print("\nYouTube Video Automation - Examples")
    print("=" * 60)

    # Choose which example to run
    examples = {
        "1": ("Create simple video", create_simple_video),
        "2": ("Create and upload to YouTube", create_and_upload),
        "3": ("Create multilingual videos", create_multilingual_video),
        "4": ("List available voices", list_available_voices),
    }

    print("\nAvailable examples:")
    for key, (name, _) in examples.items():
        print(f"{key}. {name}")

    choice = input("\nEnter example number (or 'all' to run all): ").strip()

    if choice.lower() == "all":
        for name, func in examples.values():
            print(f"\n{'=' * 60}")
            print(f"Running: {name}")
            print(f"{'=' * 60}\n")
            try:
                await func()
            except Exception as e:
                print(f"Error: {e}")
    elif choice in examples:
        name, func = examples[choice]
        print(f"\nRunning: {name}\n")
        try:
            await func()
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    asyncio.run(main())
