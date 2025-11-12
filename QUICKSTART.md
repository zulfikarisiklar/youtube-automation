# Quick Start Guide 🚀

Get started with YouTube Video Automation in 5 minutes!

## Step 1: Install Dependencies

```bash
# Install FFmpeg (if not already installed)
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Install Python packages
pip install -r requirements.txt
```

## Step 2: Configure API Keys

Run the setup wizard:

```bash
python cli.py setup
```

Or manually create a `.env` file:

```bash
cp .env.example .env
# Edit .env with your API keys
```

### Get Your API Keys:

1. **ElevenLabs** (required for audio): https://elevenlabs.io/
2. **Google AI** (for Veo): https://ai.google.dev/
3. **OpenAI** (for Sora): https://platform.openai.com/
4. **YouTube**: https://console.cloud.google.com/
   - Enable YouTube Data API v3
   - Create OAuth2 credentials
   - Download `client_secrets.json`

## Step 3: Create Your First Video

### Simple video without upload:

```bash
python cli.py create \
  --prompt "A beautiful sunset over the ocean" \
  --audio-text "Watch this stunning sunset" \
  --model veo
```

### Create and upload to YouTube:

```bash
python cli.py upload \
  --prompt "A peaceful forest with morning mist" \
  --title "Peaceful Forest Meditation" \
  --description "Relax with this AI-generated forest scene" \
  --tags "nature,relaxation,meditation" \
  --audio-text "Breathe deeply and relax" \
  --privacy private
```

## Step 4: Try Batch Processing

Create multiple videos at once:

```bash
python cli.py batch examples/batch_config.json
```

To upload them automatically:

```bash
python cli.py batch examples/batch_config.json --upload-videos
```

## Common Commands

### List available voices:
```bash
python cli.py voices
```

### List supported languages:
```bash
python cli.py languages
```

### Check system status:
```bash
python cli.py info
```

## Multi-Language Examples

### Spanish:
```bash
python cli.py create \
  --prompt "Un hermoso atardecer en la playa" \
  --audio-text "Disfruta de este hermoso atardecer" \
  --language es
```

### French:
```bash
python cli.py create \
  --prompt "Un magnifique coucher de soleil sur la mer" \
  --audio-text "Profitez de ce magnifique coucher de soleil" \
  --language fr
```

### German:
```bash
python cli.py create \
  --prompt "Ein wunderschöner Sonnenuntergang am Meer" \
  --audio-text "Genießen Sie diesen wunderschönen Sonnenuntergang" \
  --language de
```

## Python API Example

```python
import asyncio
from video_automation import VideoAutomation
from models import VideoRequest, AudioRequest

async def main():
    automation = VideoAutomation()
    automation.initialize(video_model="veo")

    video_request = VideoRequest(
        prompt="A cute puppy playing in the park",
        model="veo",
        duration=5
    )

    audio_request = AudioRequest(
        text="Look at this adorable puppy!",
        language="en"
    )

    video_path = await automation.create_video(
        video_request=video_request,
        audio_request=audio_request
    )

    print(f"Video created: {video_path}")

asyncio.run(main())
```

## Troubleshooting

### "API key not configured"
- Run `python cli.py setup` again
- Check your `.env` file has correct API keys

### "FFmpeg not found"
- Install FFmpeg: `sudo apt-get install ffmpeg` (Ubuntu) or `brew install ffmpeg` (macOS)

### "YouTube upload failed"
- Ensure `client_secrets.json` is in the project directory
- Check YouTube API is enabled in Google Cloud Console
- Verify OAuth consent screen is configured

### "Video generation failed"
- Veo and Sora APIs may have limited availability
- Check your API quotas and limits
- Verify API keys are valid

## Next Steps

1. Check out `examples/simple_example.py` for basic usage
2. Try `examples/advanced_example.py` for advanced features
3. Read the full `README.md` for detailed documentation
4. Customize `examples/batch_config.json` for your needs

## Tips

- Start with `--privacy private` until you're ready to publish
- Test with short durations (5-10 seconds) to save API costs
- Use batch processing for multiple videos to save time
- Different voices work better for different languages
- Always label AI-generated content appropriately

## Support

- Issues: Open a GitHub issue
- Examples: Check the `examples/` directory
- Documentation: See `README.md`

Happy automating! 🎬✨
