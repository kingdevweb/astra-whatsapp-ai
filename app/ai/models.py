"""Multi-model AI router — Groq (FREE), GPT, Gemini, Claude."""
from app.config import settings
from app.utils.logger import logger

SYSTEM = """Tu es Astra, un assistant IA comme ChatGPT sur WhatsApp.

CAPACITES:
- Chat intelligent sur TOUS les sujets (science, maths, code, histoire, conseils, etc.)
- Reponses dans la langue de l'utilisateur (Creole Haitien, Francais, Anglais, Espagnol...)
- Tu peux analyser, expliquer, traduire, coder, calculer, conseiller...
- Si on te demande une image dis "Tape foto [description] pour generer une image!"

REGLES:
- JAMAIS mentionner d'erreurs techniques, quotas, API, ou modeles
- JAMAIS dire "je ne peux pas" sans proposer une alternative
- Reponds TOUJOURS dans la langue de l'utilisateur
- Concis mais complet (max 1500 caracteres sur WhatsApp)
- Sympa, chaleureux, utilise des emojis de temps en temps
- Si tu ne sais pas, dis-le honnetement et propose une alternative utile"""

class AIModelRouter:
    def __init__(self):
        self.models = {}
        self.default_model = settings.ai_default_model
        
        # Groq — FREE, FAST, PRIMARY
        if settings.groq_api_key:
            try:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(
                    api_key=settings.groq_api_key,
                    base_url="https://api.groq.com/openai/v1"
                )
                self.models["groq"] = client
                self.models["llama-3.3-70b-versatile"] = "groq"
                self.models["llama-3.1-8b-instant"] = "groq"
                self.models["gemma2-9b-it"] = "groq"
                self.models["qwen-qwq-32b"] = "groq"
                logger.info("Groq ready (Llama 3.3 70B + 8B Instant + Gemma2)")
            except Exception as e: logger.warning(f"Groq init: {e}")
        
        # OpenAI — backup for image generation mainly
        if settings.openai_api_key:
            try:
                from openai import AsyncOpenAI
                self.models["openai"] = AsyncOpenAI(api_key=settings.openai_api_key)
                self.models["gpt-4o"] = "openai"
                self.models["gpt-4o-mini"] = "openai"
                logger.info("OpenAI ready (backup)")
            except Exception as e: logger.warning(f"OpenAI: {e}")
        
        # Gemini
        if settings.gemini_api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.gemini_api_key)
                self.models["gemini"] = genai
                self.models["gemini-2.5-pro"] = "gemini"
                logger.info("Gemini ready")
            except Exception as e: logger.warning(f"Gemini: {e}")
        
        # Claude
        if settings.claude_api_key:
            try:
                from anthropic import AsyncAnthropic
                self.models["claude"] = AsyncAnthropic(api_key=settings.claude_api_key)
                self.models["claude-4-sonnet"] = "claude"
                logger.info("Claude ready")
            except Exception as e: logger.warning(f"Claude: {e}")
        
        # DeepSeek
        if settings.deepseek_api_key:
            try:
                from openai import AsyncOpenAI
                self.models["deepseek"] = AsyncOpenAI(api_key=settings.deepseek_api_key, base_url="https://api.deepseek.com/v1")
                self.models["deepseek-v3"] = "deepseek"
                logger.info("DeepSeek ready")
            except Exception as e: logger.warning(f"DeepSeek: {e}")
        
        # OpenRouter
        if settings.openrouter_api_key:
            try:
                from openai import AsyncOpenAI
                self.models["openrouter"] = AsyncOpenAI(api_key=settings.openrouter_api_key, base_url="https://openrouter.ai/api/v1")
                logger.info("OpenRouter ready")
            except Exception as e: logger.warning(f"OpenRouter: {e}")

    def get_available(self) -> list:
        return [k for k in self.models if k not in ("groq","openai","gemini","claude","deepseek","openrouter")]

    async def chat(self, prompt: str, model: str = "", system: str = "", max_tokens: int = 2048, temperature: float = 0.9) -> str:
        model = model or self.default_model
        tried = []
        
        # Try all available models until one works
        fallback_order = [
            "llama-3.3-70b-versatile", "gemma2-9b-it", "llama-3.1-8b-instant",
            "gpt-4o", "gpt-4o-mini", "claude-4-sonnet", "gemini-2.5-pro", "deepseek-v3"
        ]
        
        if model in self.models:
            fallback_order.insert(0, model)
        
        last_error = ""
        for m in fallback_order:
            if m in tried: continue
            model_key = self.models.get(m, "")
            client = self.models.get(model_key)
            if not client: continue
            tried.append(m)
            
            try:
                if model_key in ("groq", "openai", "deepseek", "openrouter"):
                    resp = await client.chat.completions.create(
                        model=m,
                        messages=[
                            {"role": "system", "content": system or SYSTEM},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=max_tokens,
                        temperature=temperature,
                    )
                    return resp.choices[0].message.content
                        
                elif model_key == "gemini":
                    resp = client.GenerativeModel(model_name="gemini-pro").generate_content(
                        f"{system or SYSTEM}\n\nUser: {prompt}"
                    )
                    return resp.text
                        
                elif model_key == "claude":
                    resp = await client.messages.create(
                        model="claude-4-sonnet-20250514",
                        max_tokens=max_tokens,
                        system=system or SYSTEM,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    return resp.content[0].text
                    
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Model {m} failed: {last_error[:100]}")
                continue  # Try next model
        
        # All models failed
        logger.error(f"All models failed. Last error: {last_error}")
        return (
            "Desole, tout sistem IA yo pa disponib pou kounye a.\n\n"
            "Eseye koman sa yo pandan w ap tann:\n"
            "tan [vil] -- Meteyo\n"
            "tradwi [teks] -- Tradiksyon\n"
            "rechèch [sije] -- Google Search\n\n"
            "Nou travay pou rezoud pwoblem nan. Mersi pou pasyans ou!"
        )

    async def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        """Generate image -- tries free API first, then OpenAI."""
        # Try pollinations.ai (free, no key needed)
        try:
            import httpx
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(
                    "https://image.pollinations.ai/prompt/" + prompt.replace(" ", "%20"),
                    params={"width": 1024, "height": 1024, "nologo": "true"}
                )
                if resp.status_code == 200 and resp.headers.get("content-type","").startswith("image/"):
                    return str(resp.url)
        except: pass
        
        # Fallback to OpenAI DALL-E
        if "openai" in self.models:
            try:
                resp = await self.models["openai"].images.generate(
                    model="dall-e-3", prompt=prompt, size=size, n=1
                )
                return resp.data[0].url
            except Exception as e: logger.error(f"DALL-E: {e}")
        return ""

    def has_model(self, key: str) -> bool:
        return key in self.models

ai = AIModelRouter()
