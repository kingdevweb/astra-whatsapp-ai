"""Translation — 100+ languages."""
import httpx
from app.utils.logger import logger

async def translate_text(text: str, target: str = "en", source: str = "auto") -> dict:
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post("https://translate.googleapis.com/translate_a/single", params={"client":"gtx","sl":source,"tl":target,"dt":"t","q":text[:5000]})
            data = r.json()
            translated = "".join([s[0] for s in data[0] if s[0]])
            return {"original": text[:200], "translated": translated, "target": target}
    except Exception as e: return {"error": str(e)}
