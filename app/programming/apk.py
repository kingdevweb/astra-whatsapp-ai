"""APK/mobile app generation."""
from app.ai.models import ai
from app.prompts import CODE_PROMPT

async def create_apk(desc: str, framework: str = "react-native") -> dict:
    code = await ai.chat(prompt=f"Complete {framework} app:\n{desc}\nInclude package.json, App.js, styles.", system=CODE_PROMPT, max_tokens=4096)
    return {"framework": framework, "code": code, "status": "Generated. Build: npx react-native run-android"}
