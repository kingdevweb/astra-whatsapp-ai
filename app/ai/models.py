"""Multi-model AI router — GPT, Gemini, Claude, DeepSeek, Grok, OpenRouter."""
from app.config import settings
from app.utils.logger import logger

class AIModelRouter:
    def __init__(self):
        self.models = {}
        if settings.openai_api_key:
            try:
                from openai import AsyncOpenAI
                self.models["openai"] = AsyncOpenAI(api_key=settings.openai_api_key)
                self.models["gpt-4o"] = "openai"; self.models["gpt-5"] = "openai"
                logger.info("✅ OpenAI ready")
            except Exception as e: logger.warning(f"OpenAI: {e}")
        if settings.gemini_api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.gemini_api_key)
                self.models["gemini"] = genai; self.models["gemini-2.5-pro"] = "gemini"
                logger.info("✅ Gemini ready")
            except Exception as e: logger.warning(f"Gemini: {e}")
        if settings.claude_api_key:
            try:
                from anthropic import AsyncAnthropic
                self.models["claude"] = AsyncAnthropic(api_key=settings.claude_api_key)
                self.models["claude-4-sonnet"] = "claude"
                logger.info("✅ Claude ready")
            except Exception as e: logger.warning(f"Claude: {e}")
        if settings.deepseek_api_key:
            try:
                from openai import AsyncOpenAI
                self.models["deepseek"] = AsyncOpenAI(api_key=settings.deepseek_api_key, base_url="https://api.deepseek.com/v1")
                self.models["deepseek-v3"] = "deepseek"
                logger.info("✅ DeepSeek ready")
            except Exception as e: logger.warning(f"DeepSeek: {e}")
        if settings.grok_api_key:
            try:
                from openai import AsyncOpenAI
                self.models["grok"] = AsyncOpenAI(api_key=settings.grok_api_key, base_url="https://api.x.ai/v1")
                self.models["grok-3"] = "grok"
                logger.info("✅ Grok ready")
            except Exception as e: logger.warning(f"Grok: {e}")
        if settings.openrouter_api_key:
            try:
                from openai import AsyncOpenAI
                self.models["openrouter"] = AsyncOpenAI(api_key=settings.openrouter_api_key, base_url="https://openrouter.ai/api/v1")
                logger.info("✅ OpenRouter ready (250+ models)")
            except Exception as e: logger.warning(f"OpenRouter: {e}")

    def get_available_models(self) -> list:
        return [k for k in self.models if k not in ("openai","gemini","claude","deepseek","grok","openrouter")]

    async def chat(self, prompt: str, model: str = "", system: str = "", max_tokens: int = 1024, temperature: float = 0.7) -> str:
        model = model or settings.ai_default_model
        model_key = self.models.get(model, "")
        client = self.models.get(model_key)
        if not client:
            for m in ["gpt-4o","gemini-2.5-pro","claude-4-sonnet","deepseek-v3","grok-3"]:
                if m in self.models: model = m; model_key = self.models[m]; client = self.models.get(model_key); break
        if not client: return "⚠️ No AI models configured. Add API keys in .env"
        try:
            if model_key in ("openai","deepseek","grok","openrouter"):
                resp = await client.chat.completions.create(model=model, messages=[{"role":"system","content":system or "You are Astra."},{"role":"user","content":prompt}], max_tokens=max_tokens, temperature=temperature)
                return resp.choices[0].message.content
            elif model_key == "gemini":
                resp = client.GenerativeModel(model_name="gemini-pro").generate_content(prompt)
                return resp.text
            elif model_key == "claude":
                resp = await client.messages.create(model="claude-4-sonnet-20250514", max_tokens=max_tokens, system=system or "You are Astra.", messages=[{"role":"user","content":prompt}])
                return resp.content[0].text
        except Exception as e: logger.error(f"AI error ({model}): {e}"); return f"⚠️ {model} error: {e}"

    async def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        if "openai" in self.models:
            try:
                resp = await self.models["openai"].images.generate(model="dall-e-3", prompt=prompt, size=size, n=1)
                return resp.data[0].url
            except Exception as e: logger.error(f"Image gen: {e}")
        return "⚠️ OpenAI API key required for image generation"

    def has_model(self, key: str) -> bool: return key in self.models

ai = AIModelRouter()
