#!/usr/bin/env python3
"""Advanced example showcasing video processing features."""
import asyncio
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from video_automation import VideoAutomation
from models import VideoRequest, AudioRequest
from video_processor import VideoProcessor


async def create_video_with_text_overlay():
    """Create a video and add text overlay."""
    print("Creating video with text overlay...")

    automation = VideoAutomation()
    automation.initialize(video_model="veo")

    # Create video
    video_request = VideoRequest(
        prompt="A motivational sunrise scene",
        model="veo",
        duration=5
    )

    video_path = await automation.create_video(
        video_request=video_request,
        output_path=Path("output/sunrise_base.mp4")
    )

    # Add text overlay
    processor = VideoProcessor()
    final_path = await processor.add_text_overlay(
        video_path=video_path,
        text="Start Your Day Right!",
        output_path=Path("output/sunrise_with_text.mp4"),
        position=('center', 'bottom'),
        fontsize=60,
        color='white'
    )

    print(f"\nVideo with text overlay created: {final_path}")


async def create_concatenated_video():
    """Create multiple videos and concatenate them."""
    print("Creating concatenated video from multiple clips...")

    automation = VideoAutomation()
    automation.initialize(video_model="veo")

    # Create multiple video clips
    prompts = [
        "A sunrise over mountains",
        "A flowing river through a valley",
        "A sunset over the ocean"
    ]

    video_paths = []
    for i, prompt in enumerate(prompts, 1):
        print(f"\nCreating clip {i}/{len(prompts)}: {prompt}")

        video_request = VideoRequest(
            prompt=prompt,
            model="veo",
            duration=3
        )

        video_path = await automation.create_video(
            video_request=video_request,
            output_path=Path(f"output/clip_{i}.mp4")
        )

        video_paths.append(video_path)

    # Concatenate videos
    print("\nConcatenating videos...")
    processor = VideoProcessor()
    final_path = await processor.concatenate_videos(
        video_paths=video_paths,
        output_path=Path("output/nature_journey.mp4")
    )

    print(f"\nConcatenated video created: {final_path}")


async def create_multi_language_series():
    """Create a series of videos in different languages."""
    print("Creating multi-language video series...")

    automation = VideoAutomation()
    automation.initialize(video_model="veo")

    # Content in different languages
    content = {
        "en": {
            "prompt": "A chef cooking in a modern kitchen",
            "audio": "Learn how to cook delicious meals with our recipes",
            "title": "Cooking Tutorial - Easy Recipes"
        },
        "es": {
            "prompt": "Un chef cocinando en una cocina moderna",
            "audio": "Aprende a cocinar comidas deliciosas con nuestras recetas",
            "title": "Tutorial de Cocina - Recetas Fáciles"
        },
        "fr": {
            "prompt": "Un chef cuisinant dans une cuisine moderne",
            "audio": "Apprenez à cuisiner de délicieux repas avec nos recettes",
            "title": "Tutoriel de Cuisine - Recettes Faciles"
        },
        "de": {
            "prompt": "Ein Koch, der in einer modernen Küche kocht",
            "audio": "Lernen Sie mit unseren Rezepten köstliche Mahlzeiten zu kochen",
            "title": "Kochkurs - Einfache Rezepte"
        }
    }

    for lang, data in content.items():
        print(f"\nCreating video in {lang}...")

        video_request = VideoRequest(
            prompt=data["prompt"],
            model="veo",
            duration=5
        )

        audio_request = AudioRequest(
            text=data["audio"],
            language=lang
        )

        video_path = await automation.create_video(
            video_request=video_request,
            audio_request=audio_request,
            output_path=Path(f"output/cooking_{lang}.mp4")
        )

        print(f"Created {lang} version: {video_path}")


async def create_video_with_custom_voice():
    """Create video with a specific ElevenLabs voice."""
    print("Creating video with custom voice...")

    automation = VideoAutomation()
    automation.initialize(video_model="veo")

    # List available voices
    print("\nAvailable voices:")
    voices = automation.list_available_voices()
    for i, voice in enumerate(voices[:5], 1):
        print(f"{i}. {voice['name']} ({voice['voice_id']})")

    # Use a specific voice (or default)
    voice_id = voices[0]['voice_id'] if voices else None

    video_request = VideoRequest(
        prompt="A professional news anchor in a studio",
        model="veo",
        duration=5
    )

    audio_request = AudioRequest(
        text="Good evening, welcome to our daily news broadcast",
        language="en",
        voice_id=voice_id
    )

    video_path = await automation.create_video(
        video_request=video_request,
        audio_request=audio_request,
        output_path=Path("output/news_broadcast.mp4")
    )

    print(f"\nVideo with custom voice created: {video_path}")


async def batch_processing_with_error_handling():
    """Demonstrate batch processing with error handling."""
    print("Batch processing with error handling...")

    automation = VideoAutomation()
    automation.initialize(video_model="veo")

    # Mix of valid and potentially problematic requests
    requests = [
        {
            "prompt": "A beautiful garden with colorful flowers",
            "audio": "Enjoy the beauty of nature",
            "name": "garden"
        },
        {
            "prompt": "A futuristic city with flying cars",
            "audio": "Welcome to the future",
            "name": "future_city"
        },
        {
            "prompt": "An underwater coral reef with tropical fish",
            "audio": "Explore the wonders of the ocean",
            "name": "coral_reef"
        }
    ]

    results = []
    for i, req in enumerate(requests, 1):
        print(f"\nProcessing video {i}/{len(requests)}: {req['name']}")

        try:
            video_request = VideoRequest(
                prompt=req["prompt"],
                model="veo",
                duration=5
            )

            audio_request = AudioRequest(
                text=req["audio"],
                language="en"
            )

            video_path = await automation.create_video(
                video_request=video_request,
                audio_request=audio_request,
                output_path=Path(f"output/{req['name']}.mp4")
            )

            results.append({
                "name": req["name"],
                "success": True,
                "path": video_path
            })

            print(f"✓ Success: {req['name']}")

        except Exception as e:
            results.append({
                "name": req["name"],
                "success": False,
                "error": str(e)
            })

            print(f"✗ Failed: {req['name']} - {str(e)}")

    # Summary
    print("\n" + "=" * 60)
    print("BATCH PROCESSING SUMMARY")
    print("=" * 60)
    successful = sum(1 for r in results if r["success"])
    print(f"Successful: {successful}/{len(results)}")
    print(f"Failed: {len(results) - successful}/{len(results)}")


async def main():
    """Main function to run advanced examples."""
    print("\nYouTube Video Automation - Advanced Examples")
    print("=" * 60)

    examples = {
        "1": ("Video with text overlay", create_video_with_text_overlay),
        "2": ("Concatenated video", create_concatenated_video),
        "3": ("Multi-language series", create_multi_language_series),
        "4": ("Custom voice video", create_video_with_custom_voice),
        "5": ("Batch processing with error handling", batch_processing_with_error_handling),
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
            await asyncio.sleep(2)  # Small delay between examples
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
