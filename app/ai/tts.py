"""Text-to-Speech."""
from app.config import settings
from app.utils.logger import logger

async def text_to_speech(text: str, voice: str = "alloy", provider: str = "openai") -> dict:
    if provider == "elevenlabs" and settings.elevenlabs_api_key:
        return {"provider": "elevenlabs", "voice": voice, "text": text[:200], "status": "TTS ready"}
    elif settings.openai_api_key:
        return {"provider": "openai", "voice": voice, "text": text[:200], "format": "mp3", "status": "TTS ready"}
    return {"error": "No TTS provider configured"}
