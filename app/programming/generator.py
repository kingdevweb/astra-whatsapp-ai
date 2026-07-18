"""Code gen, debug, explain, refactor."""
from app.ai.models import ai
from app.prompts import CODE_PROMPT

async def generate_code(spec: str, lang: str = "python", framework: str = "") -> str:
    fw = f" using {framework}" if framework else ""
    return await ai.chat(prompt=f"Generate production {lang}{fw} code:\n{spec}", system=CODE_PROMPT, max_tokens=2048)

async def debug_code(code: str, error: str = "") -> str:
    e = f"\nError: {error}" if error else ""
    return await ai.chat(prompt=f"Debug & fix:\n```\n{code}\n```{e}\nProvide fixed code + explanation.", system=CODE_PROMPT, max_tokens=2048)

async def explain_code(code: str) -> str:
    return await ai.chat(prompt=f"Explain this code simply:\n```\n{code}\n```", system=CODE_PROMPT)

async def refactor_code(code: str, goal: str = "improve readability & performance") -> str:
    return await ai.chat(prompt=f"Refactor to {goal}:\n```\n{code}\n```\nGive refactored code + explanation.", system=CODE_PROMPT, max_tokens=2048)
