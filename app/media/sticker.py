"""Sticker maker."""
from PIL import Image
import os

async def make_sticker(image_path: str, output_path: str = "") -> dict:
    try:
        img = Image.open(image_path); img.thumbnail((512,512), Image.LANCZOS)
        sticker = Image.new("RGBA",(512,512),(0,0,0,0))
        sticker.paste(img.convert("RGBA"),((512-img.width)//2,(512-img.height)//2))
        out = output_path or f"{os.path.splitext(image_path)[0]}.webp"
        sticker.save(out,"WEBP",quality=90)
        return {"status":"created","path":out,"size":"512x512"}
    except Exception as e: return {"error": str(e)}
