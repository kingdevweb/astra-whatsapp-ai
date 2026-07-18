"""Website generator."""
from app.ai.models import ai
from app.prompts import CODE_PROMPT

async def create_website(spec: str, stack: str = "html-tailwind") -> dict:
    code = await ai.chat(prompt=f"Complete {stack} website:\n{spec}\nResponsive, modern, production-ready.", system=CODE_PROMPT, max_tokens=4096)
    return {"stack": stack, "code": code, "status": "Website generated"}
