"""Avatar generator."""
from app.ai.models import ai

async def generate_avatar(description: str = "professional headshot", style: str = "cartoon") -> dict:
    url = await ai.generate_image(prompt=f"{style} avatar, {description}, clean bg, 512x512")
    return {"url": url, "style": style}
