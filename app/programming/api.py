"""REST API generator."""
from app.ai.models import ai
from app.prompts import CODE_PROMPT

async def create_api(spec: str, framework: str = "fastapi") -> dict:
    code = await ai.chat(prompt=f"Complete {framework} API:\n{spec}\nInclude models, routes, DB, error handling.", system=CODE_PROMPT, max_tokens=4096)
    return {"framework": framework, "code": code, "status": "API generated"}
