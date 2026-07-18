"""News search."""
import httpx
from app.utils.logger import logger

async def get_news(topic: str = "", max_results: int = 5) -> list[dict]:
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            u = "https://news.google.com/rss" if not topic else f"https://news.google.com/rss/search?q={topic}"
            r = await c.get(u)
            import xml.etree.ElementTree as ET
            root = ET.fromstring(r.text)
            return [{"title": i.findtext("title",""), "link": i.findtext("link",""), "date": i.findtext("pubDate","")} for i in list(root.iter("item"))[:max_results]]
    except Exception as e: logger.error(f"News: {e}"); return [{"title":"News unavailable","error":str(e)}]
