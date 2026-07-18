"""Image generation & editing."""
from app.ai.models import ai
async def generate(prompt: str, style: str = "realistic", size: str = "1024x1024") -> dict:
    fp = f"{prompt}, {style} style, high quality, detailed"
    url = await ai.generate_image(prompt=fp, size=size)
    return {"url": url, "prompt": fp, "style": style}
async def edit(image_url: str, edit_prompt: str) -> dict:
    return {"url": image_url, "prompt": edit_prompt, "status": "Use DALL-E edit endpoint"}
