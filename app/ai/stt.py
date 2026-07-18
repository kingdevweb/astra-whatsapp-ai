"""Speech-to-Text — Whisper."""
from app.config import settings
from app.utils.logger import logger

async def transcribe(audio_path: str, language: str = "auto") -> dict:
    if not settings.openai_api_key: return {"error": "OpenAI key required"}
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        with open(audio_path, "rb") as f:
            t = await client.audio.transcriptions.create(model="whisper-1", file=f, language=None if language=="auto" else language)
        return {"text": t.text, "language": getattr(t,"language",language)}
    except Exception as e: logger.error(f"STT: {e}"); return {"error": str(e)}
