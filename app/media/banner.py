"""Banner/flyer generator."""
from app.ai.models import ai

async def generate_banner(title: str, subtitle: str = "", style: str = "modern", purpose: str = "social media") -> dict:
    prompt = f"{style} {purpose} banner, title '{title}'" + (f", subtitle '{subtitle}'" if subtitle else "") + ", professional, 1200x628"
    url = await ai.generate_image(prompt=prompt, size="1792x1024")
    return {"url": url, "title": title, "style": style}
