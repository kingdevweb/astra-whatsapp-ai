"""Web search via DuckDuckGo."""
import httpx
from app.utils.logger import logger

async def web_search(query: str, max_results: int = 5) -> list[dict]:
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get("https://api.duckduckgo.com/", params={"q": query, "format": "json", "no_html": 1})
            data = r.json()
            results = []
            if data.get("AbstractText"):
                results.append({"title": data.get("AbstractSource",""), "snippet": data["AbstractText"], "url": data.get("AbstractURL","")})
            for t in data.get("RelatedTopics", [])[:max_results]:
                if isinstance(t, dict) and t.get("Text"):
                    results.append({"title": t.get("FirstURL","").split("/")[-1], "snippet": t["Text"], "url": t.get("FirstURL","")})
            return results[:max_results]
    except Exception as e: logger.error(f"Search: {e}"); return [{"title":"Error","snippet":str(e)}]

async def news_search(topic: str = "", max_results: int = 5) -> list[dict]:
    return await web_search(f"news {topic or 'latest'}", max_results)
