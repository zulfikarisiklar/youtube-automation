# YouTube Video Automation 🎬

Automated YouTube video generation and upload system using AI models (Google Veo, OpenAI Sora) with multi-language audio support (ElevenLabs).

## Features

- 🎥 **Multiple AI Video Models**: Support for Google Veo and OpenAI Sora
- 🎙️ **Multi-Language Audio**: Generate voiceovers in 30+ languages using ElevenLabs
- 🔄 **Automated Workflow**: Generate video, add audio, and upload to YouTube
- 📦 **Batch Processing**: Process multiple videos from a configuration file
- 🎨 **Video Processing**: Merge audio/video, add text overlays, resize, and concatenate
- 🚀 **Easy CLI**: Simple command-line interface for all operations
- 🔌 **Extensible**: Easy to add new video generation models

## Installation

### Prerequisites

- Python 3.9 or higher
- FFmpeg (for video processing)

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Setup

### 1. Run Setup Wizard

```bash
python cli.py setup
```

This will guide you through configuring your API keys.

### 2. Manual Configuration

Alternatively, copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_AI_API_KEY=your_google_ai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# YouTube API Credentials
YOUTUBE_CLIENT_SECRETS_FILE=client_secrets.json
```

### 3. Get API Keys

#### OpenAI (for Sora)
- Visit: https://platform.openai.com/api-keys
- Note: Sora API may require waitlist access

#### Google AI (for Veo)
- Visit: https://ai.google.dev/
- Note: Veo API availability may vary by region

#### ElevenLabs (for Audio)
- Visit: https://elevenlabs.io/
- Sign up and get your API key from the dashboard

#### YouTube Data API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "YouTube Data API v3"
4. Create OAuth 2.0 credentials
5. Download the JSON file and save as `client_secrets.json`

## Usage

### Quick Start

#### Create a video with audio:

```bash
python cli.py create \
  --prompt "A serene sunset over mountains" \
  --audio-text "Watch this beautiful sunset over the mountains" \
  --language en \
  --model veo \
  --duration 5
```

#### Create and upload to YouTube:

```bash
python cli.py upload \
  --prompt "A cat playing with a ball" \
  --title "Cute Cat Playing" \
  --description "AI-generated video of a playful cat" \
  --tags "cat,animals,ai,cute" \
  --audio-text "Look at this adorable cat playing" \
  --privacy private
```

### Available Commands

#### `create` - Create a video

```bash
python cli.py create [OPTIONS]

Options:
  -p, --prompt TEXT          Video generation prompt [required]
  -m, --model [veo|sora]    Video generation model (default: veo)
  -d, --duration INTEGER     Video duration in seconds (default: 5)
  -a, --audio-text TEXT     Text for audio generation
  -l, --language TEXT       Audio language code (default: en)
  --voice-id TEXT           ElevenLabs voice ID
  -o, --output TEXT         Output file path
```

#### `upload` - Create and upload to YouTube

```bash
python cli.py upload [OPTIONS]

Options:
  -p, --prompt TEXT              Video generation prompt [required]
  -t, --title TEXT              YouTube video title [required]
  --description TEXT            YouTube video description
  --tags TEXT                   Comma-separated tags
  -m, --model [veo|sora]        Video generation model
  -d, --duration INTEGER         Video duration in seconds
  -a, --audio-text TEXT         Text for audio generation
  -l, --language TEXT           Audio language code
  --voice-id TEXT               ElevenLabs voice ID
  --privacy [public|private|unlisted]  Privacy status (default: private)
  --category TEXT               YouTube category ID (default: 22)
```

#### `batch` - Process multiple videos

```bash
python cli.py batch config.json [--upload-videos]
```

See `examples/batch_config.json` for configuration format.

#### `voices` - List available voices

```bash
python cli.py voices
```

#### `languages` - List supported languages

```bash
python cli.py languages
```

#### `info` - Display system information

```bash
python cli.py info
```

### Supported Languages

ElevenLabs supports 30+ languages including:
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Polish (pl)
- Hindi (hi)
- Arabic (ar)
- Chinese (zh)
- Japanese (ja)
- Korean (ko)
- And many more...

## Python API

You can also use the library programmatically:

```python
import asyncio
from video_automation import VideoAutomation
from models import VideoRequest, AudioRequest, YouTubeMetadata

async def main():
    # Initialize
    automation = VideoAutomation()
    automation.initialize(video_model="veo")

    # Create video request
    video_request = VideoRequest(
        prompt="A peaceful forest with sunlight streaming through trees",
        model="veo",
        duration=5
    )

    # Create audio request
    audio_request = AudioRequest(
        text="Experience the tranquility of nature",
        language="en"
    )

    # Create YouTube metadata
    youtube_metadata = YouTubeMetadata(
        title="Peaceful Forest",
        description="AI-generated nature video",
        tags=["nature", "forest", "ai"],
        privacy_status="private"
    )

    # Create and upload
    result = await automation.create_and_upload(
        video_request=video_request,
        youtube_metadata=youtube_metadata,
        audio_request=audio_request
    )

    print(f"Video uploaded: {result['url']}")

asyncio.run(main())
```

## Batch Processing

Create a JSON configuration file for batch processing:

```json
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
  },
  {
    "video_request": {
      "prompt": "Ocean waves crashing on the beach",
      "model": "veo",
      "duration": 5
    },
    "audio_request": {
      "text": "Relax to the sound of ocean waves",
      "language": "en"
    },
    "youtube_metadata": {
      "title": "Ocean Waves",
      "description": "Relaxing ocean video",
      "tags": ["ocean", "waves", "relaxation"],
      "privacy_status": "private"
    }
  }
]
```

Run batch processing:

```bash
python cli.py batch examples/batch_config.json --upload-videos
```

## Video Processing Features

The system includes powerful video processing utilities:

- **Merge Audio and Video**: Automatically sync audio with video
- **Add Text Overlays**: Add captions or titles to videos
- **Resize Videos**: Change resolution and aspect ratio
- **Concatenate Videos**: Combine multiple videos into one

## Project Structure

```
youtube-automation/
├── cli.py                    # Command-line interface
├── config.py                 # Configuration management
├── models.py                 # Data models
├── video_automation.py       # Main orchestrator
├── audio_generator.py        # ElevenLabs integration
├── video_processor.py        # Video processing utilities
├── youtube_uploader.py       # YouTube upload functionality
├── video_generators/
│   ├── __init__.py
│   ├── base.py              # Base video generator class
│   ├── veo.py               # Google Veo implementation
│   └── sora.py              # OpenAI Sora implementation
├── requirements.txt          # Python dependencies
├── .env.example             # Example configuration
└── examples/
    └── batch_config.json    # Example batch configuration
```

## Extending the System

### Adding a New Video Model

1. Create a new generator class in `video_generators/`:

```python
from .base import VideoGenerator

class MyModelGenerator(VideoGenerator):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        # Initialize your model

    def get_model_name(self) -> str:
        return "mymodel"

    async def generate(self, prompt: str, **kwargs) -> Path:
        # Implement video generation
        pass
```

2. Register it in `video_generators/__init__.py`

3. Update `video_automation.py` to support the new model

## Troubleshooting

### FFmpeg Not Found
Make sure FFmpeg is installed and in your PATH.

### API Authentication Errors
- Verify your API keys in `.env`
- Check API quotas and limits
- Ensure APIs are enabled in respective platforms

### YouTube Upload Fails
- Ensure `client_secrets.json` is correctly configured
- Check YouTube API quota (default is 10,000 units/day)
- Verify OAuth consent screen is configured

### Video Generation Not Available
- Veo and Sora APIs may have limited availability
- Check respective platforms for API access status
- Consider using alternative models or placeholder implementations

## Limitations

- **Sora API**: As of now, Sora API may not be publicly available. The implementation is prepared for when it becomes available.
- **Veo API**: Google Veo access may be limited. Check Google AI documentation for current status.
- **YouTube Quota**: YouTube API has daily quota limits (10,000 units by default).
- **Video Duration**: Some models may have limitations on video duration.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

MIT License - feel free to use this project for any purpose.

## Disclaimer

This project is for educational and automation purposes. Ensure you comply with:
- YouTube's Terms of Service
- ElevenLabs Terms of Service
- OpenAI and Google AI usage policies
- Content ownership and copyright laws

AI-generated content should be clearly labeled as such when uploaded to platforms.

## Support

For issues and questions:
- Open an issue on GitHub
- Check API documentation for respective services
- Review examples in the `examples/` directory

## Acknowledgments

- OpenAI for Sora video generation
- Google for Veo video generation
- ElevenLabs for multi-language audio synthesis
- YouTube Data API for video uploads
- MoviePy for video processing
