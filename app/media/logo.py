"""Logo generator."""
from app.ai.models import ai

async def generate_logo(business_name: str, industry: str = "tech", style: str = "minimal", colors: str = "blue and white") -> dict:
    prompt = f"Professional {style} logo for '{business_name}', {industry}, {colors}, vector style, white bg, no text"
    url = await ai.generate_image(prompt=prompt)
    return {"url": url, "business_name": business_name, "style": style}
