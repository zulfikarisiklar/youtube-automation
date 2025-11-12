#!/usr/bin/env python3
"""Command-line interface for YouTube video automation."""
import asyncio
import json
from pathlib import Path
import click

from video_automation import VideoAutomation
from models import VideoRequest, AudioRequest, YouTubeMetadata, VideoProject


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """YouTube Video Automation - Generate and upload AI videos to YouTube."""
    pass


@cli.command()
@click.option('--prompt', '-p', required=True, help='Video generation prompt')
@click.option('--model', '-m', type=click.Choice(['veo', 'sora']), default='veo', help='Video generation model')
@click.option('--duration', '-d', type=int, default=5, help='Video duration in seconds')
@click.option('--audio-text', '-a', help='Text for audio generation')
@click.option('--language', '-l', default='en', help='Audio language code (e.g., en, es, fr)')
@click.option('--voice-id', help='ElevenLabs voice ID')
@click.option('--output', '-o', help='Output file path')
def create(prompt, model, duration, audio_text, language, voice_id, output):
    """Create a video with optional audio."""
    async def run():
        automation = VideoAutomation()
        automation.initialize(video_model=model)

        # Create video request
        video_request = VideoRequest(
            prompt=prompt,
            model=model,
            duration=duration
        )

        # Create audio request if text provided
        audio_request = None
        if audio_text:
            audio_request = AudioRequest(
                text=audio_text,
                language=language,
                voice_id=voice_id
            )

        # Generate video
        output_path = Path(output) if output else None
        video_path = await automation.create_video(
            video_request=video_request,
            audio_request=audio_request,
            output_path=output_path
        )

        click.echo(f"\n✓ Video created: {video_path}")

    asyncio.run(run())


@cli.command()
@click.option('--prompt', '-p', required=True, help='Video generation prompt')
@click.option('--title', '-t', required=True, help='YouTube video title')
@click.option('--description', '-desc', default='', help='YouTube video description')
@click.option('--tags', help='Comma-separated tags')
@click.option('--model', '-m', type=click.Choice(['veo', 'sora']), default='veo', help='Video generation model')
@click.option('--duration', '-d', type=int, default=5, help='Video duration in seconds')
@click.option('--audio-text', '-a', help='Text for audio generation')
@click.option('--language', '-l', default='en', help='Audio language code')
@click.option('--voice-id', help='ElevenLabs voice ID')
@click.option('--privacy', type=click.Choice(['public', 'private', 'unlisted']), default='private', help='YouTube privacy status')
@click.option('--category', default='22', help='YouTube category ID')
def upload(prompt, title, description, tags, model, duration, audio_text, language, voice_id, privacy, category):
    """Create and upload a video to YouTube."""
    async def run():
        automation = VideoAutomation()
        automation.initialize(video_model=model)

        # Create video request
        video_request = VideoRequest(
            prompt=prompt,
            model=model,
            duration=duration
        )

        # Create audio request if text provided
        audio_request = None
        if audio_text:
            audio_request = AudioRequest(
                text=audio_text,
                language=language,
                voice_id=voice_id
            )

        # Create YouTube metadata
        tag_list = [tag.strip() for tag in tags.split(',')] if tags else []
        youtube_metadata = YouTubeMetadata(
            title=title,
            description=description,
            tags=tag_list,
            category_id=category,
            privacy_status=privacy,
            language=language
        )

        # Create and upload
        upload_info = await automation.create_and_upload(
            video_request=video_request,
            youtube_metadata=youtube_metadata,
            audio_request=audio_request
        )

        click.echo(f"\n✓ Video uploaded successfully!")
        click.echo(f"  URL: {upload_info['url']}")
        click.echo(f"  Video ID: {upload_info['id']}")

    asyncio.run(run())


@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.option('--upload-videos', is_flag=True, help='Upload videos to YouTube')
def batch(config_file, upload_videos):
    """Process multiple videos from a JSON configuration file.

    Example JSON format:
    [
      {
        "video_request": {
          "prompt": "A serene sunset over mountains",
          "model": "veo",
          "duration": 5
        },
        "audio_request": {
          "text": "Watch this beautiful sunset",
          "language": "en"
        },
        "youtube_metadata": {
          "title": "Beautiful Sunset",
          "description": "AI-generated sunset video",
          "tags": ["sunset", "nature", "ai"],
          "privacy_status": "private"
        }
      }
    ]
    """
    async def run():
        # Load configuration
        with open(config_file, 'r') as f:
            configs = json.load(f)

        # Parse projects
        projects = []
        for config in configs:
            project = VideoProject(**config)
            projects.append(project)

        click.echo(f"Loaded {len(projects)} projects from {config_file}")

        # Process batch
        automation = VideoAutomation()
        automation.initialize()

        results = await automation.batch_create(
            projects=projects,
            upload=upload_videos
        )

        # Display results
        click.echo("\nResults:")
        for result in results:
            if result["success"]:
                click.echo(f"  ✓ Project {result['project_index']}: Success")
            else:
                click.echo(f"  ✗ Project {result['project_index']}: {result['error']}")

    asyncio.run(run())


@cli.command()
def voices():
    """List available ElevenLabs voices."""
    async def run():
        automation = VideoAutomation()
        automation.initialize()

        voices = automation.list_available_voices()

        if not voices:
            click.echo("No voices available or failed to fetch voices.")
            return

        click.echo(f"\nAvailable Voices ({len(voices)}):")
        click.echo("-" * 60)
        for voice in voices:
            click.echo(f"  Name: {voice['name']}")
            click.echo(f"  ID: {voice['voice_id']}")
            click.echo(f"  Category: {voice['category']}")
            click.echo()

    asyncio.run(run())


@cli.command()
def languages():
    """List supported languages for audio generation."""
    async def run():
        automation = VideoAutomation()
        automation.initialize()

        languages = automation.get_supported_languages()

        click.echo(f"\nSupported Languages ({len(languages)}):")
        click.echo("-" * 60)
        for i, lang in enumerate(languages, 1):
            click.echo(f"  {lang}", nl=(i % 5 == 0))
        click.echo()

    asyncio.run(run())


@cli.command()
def setup():
    """Interactive setup wizard."""
    click.echo("\n" + "="*60)
    click.echo("YouTube Video Automation - Setup Wizard")
    click.echo("="*60 + "\n")

    # Check if .env exists
    env_path = Path(".env")
    if env_path.exists():
        if not click.confirm(".env file already exists. Overwrite?"):
            click.echo("Setup cancelled.")
            return

    click.echo("Please provide your API keys:\n")

    # OpenAI API Key
    openai_key = click.prompt("OpenAI API Key (for Sora)", default="", show_default=False)

    # Google AI API Key
    google_key = click.prompt("Google AI API Key (for Veo)", default="", show_default=False)

    # ElevenLabs API Key
    elevenlabs_key = click.prompt("ElevenLabs API Key", default="", show_default=False)

    # YouTube credentials
    click.echo("\nFor YouTube upload, you need to:")
    click.echo("1. Go to https://console.cloud.google.com/")
    click.echo("2. Enable YouTube Data API v3")
    click.echo("3. Create OAuth2 credentials")
    click.echo("4. Download the JSON file\n")

    youtube_file = click.prompt(
        "Path to YouTube client secrets JSON",
        default="client_secrets.json"
    )

    # Create .env file
    env_content = f"""# API Keys
OPENAI_API_KEY={openai_key}
GOOGLE_AI_API_KEY={google_key}
ELEVENLABS_API_KEY={elevenlabs_key}

# YouTube API Credentials
YOUTUBE_CLIENT_SECRETS_FILE={youtube_file}

# Default Settings
DEFAULT_VIDEO_MODEL=veo
DEFAULT_LANGUAGE=en
DEFAULT_VOICE_ID=

# Video Settings
VIDEO_RESOLUTION=1920x1080
VIDEO_FPS=30
MAX_VIDEO_DURATION=60

# Output Settings
OUTPUT_DIR=./output
TEMP_DIR=./temp
"""

    env_path.write_text(env_content)

    click.echo("\n✓ Configuration saved to .env")
    click.echo("\nSetup complete! You can now use the CLI commands.")
    click.echo("\nQuick start:")
    click.echo("  python cli.py create --prompt 'Your video prompt' --audio-text 'Your narration'")
    click.echo("  python cli.py upload --prompt 'Your video prompt' --title 'Video Title'")


@cli.command()
def info():
    """Display system information and configuration status."""
    from config import config

    click.echo("\n" + "="*60)
    click.echo("YouTube Video Automation - System Information")
    click.echo("="*60 + "\n")

    # Check API keys
    keys_status = config.validate_keys()

    click.echo("API Keys Status:")
    click.echo(f"  OpenAI (Sora): {'✓ Configured' if keys_status['openai'] else '✗ Not configured'}")
    click.echo(f"  Google AI (Veo): {'✓ Configured' if keys_status['google_ai'] else '✗ Not configured'}")
    click.echo(f"  ElevenLabs: {'✓ Configured' if keys_status['elevenlabs'] else '✗ Not configured'}")
    click.echo(f"  YouTube: {'✓ Configured' if keys_status['youtube'] else '✗ Not configured'}")

    click.echo(f"\nDirectories:")
    click.echo(f"  Output: {config.output_dir}")
    click.echo(f"  Temp: {config.temp_dir}")

    click.echo(f"\nDefault Settings:")
    click.echo(f"  Video Model: {config.default_video_model}")
    click.echo(f"  Language: {config.default_language}")
    click.echo(f"  Resolution: {config.video_resolution}")
    click.echo(f"  FPS: {config.video_fps}")
    click.echo(f"  Max Duration: {config.max_video_duration}s")

    click.echo()


if __name__ == '__main__':
    cli()
