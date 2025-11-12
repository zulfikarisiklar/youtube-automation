"""ElevenLabs audio generator."""
import asyncio
from pathlib import Path
from typing import Optional
from elevenlabs.client import ElevenLabs
from elevenlabs import save


class AudioGenerator:
    """ElevenLabs audio generator with multi-language support."""

    # Popular voice IDs (these are example IDs - users should use their own)
    POPULAR_VOICES = {
        "rachel": "21m00Tcm4TlvDq8ikWAM",
        "drew": "29vD33N1CtxCmqQRPOHJ",
        "clyde": "2EiwWnXFnvU5JabPnv8n",
        "paul": "5Q0t7uMcjvnagumLfvZi",
        "antoni": "ErXwobaYiN019PkySvjV",
        "josh": "TxGEqnHWrfWFTfGW9XjX",
        "arnold": "VR6AewLTigWG4xSOukaG",
        "adam": "pNInz6obpgDQGcFmaJgB",
        "sam": "yoZ06aMxZJJ28mfd3POQ",
    }

    # Language support (ElevenLabs supports many languages)
    SUPPORTED_LANGUAGES = [
        "en", "es", "fr", "de", "it", "pt", "pl", "hi", "ar", "zh", "ja", "ko", "nl", "tr", "sv", "id", "fil", "uk", "el", "cs", "fi", "ro", "ru", "da", "bg", "ms", "sk", "hr", "ta"
    ]

    def __init__(self, api_key: str):
        """Initialize audio generator.

        Args:
            api_key: ElevenLabs API key
        """
        self.api_key = api_key
        self.client = ElevenLabs(api_key=api_key)

    async def generate(
        self,
        text: str,
        language: str = "en",
        voice_id: Optional[str] = None,
        model_id: str = "eleven_multilingual_v2",
        output_path: Optional[Path] = None
    ) -> Path:
        """Generate audio from text.

        Args:
            text: Text to convert to speech
            language: Language code (e.g., "en", "es", "fr")
            voice_id: ElevenLabs voice ID (optional, will use default)
            model_id: ElevenLabs model ID
            output_path: Path to save the audio file

        Returns:
            Path to the generated audio file
        """
        if output_path is None:
            import time
            output_path = Path(f"audio_{int(time.time())}.mp3")

        if language not in self.SUPPORTED_LANGUAGES:
            print(f"Warning: Language '{language}' might not be fully supported.")
            print(f"Supported languages: {', '.join(self.SUPPORTED_LANGUAGES)}")

        # Use default voice if not specified
        if voice_id is None:
            voice_id = self.POPULAR_VOICES["rachel"]
            print(f"Using default voice: rachel")

        print(f"Generating audio in language: {language}")
        print(f"Voice ID: {voice_id}")
        print(f"Model: {model_id}")

        try:
            # Generate audio
            audio = await asyncio.to_thread(
                self._generate_sync,
                text=text,
                voice_id=voice_id,
                model_id=model_id
            )

            # Save audio
            save(audio, str(output_path))
            print(f"Audio generated successfully: {output_path}")

            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to generate audio: {str(e)}")

    def _generate_sync(self, text: str, voice_id: str, model_id: str):
        """Synchronous audio generation call.

        Args:
            text: Text to convert to speech
            voice_id: ElevenLabs voice ID
            model_id: ElevenLabs model ID

        Returns:
            Audio generator object
        """
        return self.client.generate(
            text=text,
            voice=voice_id,
            model=model_id
        )

    def list_voices(self) -> list[dict]:
        """List available voices.

        Returns:
            List of voice dictionaries
        """
        try:
            voices = self.client.voices.get_all()
            return [
                {
                    "voice_id": voice.voice_id,
                    "name": voice.name,
                    "category": voice.category if hasattr(voice, "category") else "unknown"
                }
                for voice in voices.voices
            ]
        except Exception as e:
            print(f"Failed to list voices: {str(e)}")
            return []

    def get_voice_id(self, voice_name: str) -> Optional[str]:
        """Get voice ID by name.

        Args:
            voice_name: Voice name

        Returns:
            Voice ID if found, None otherwise
        """
        # Check popular voices first
        if voice_name.lower() in self.POPULAR_VOICES:
            return self.POPULAR_VOICES[voice_name.lower()]

        # Search in available voices
        voices = self.list_voices()
        for voice in voices:
            if voice["name"].lower() == voice_name.lower():
                return voice["voice_id"]

        return None
