"""Multi-model AI router — Groq, GPT, Gemini, Claude, DeepSeek, OpenRouter."""
from app.config import settings
from app.utils.logger import logger

CHAT_SYSTEM = """Tu es Astra, un assistant IA ultra-puissant integre a WhatsApp. Tu es:

- Intelligent — comme ChatGPT, tu reponds a TOUT: science, histoire, code, maths, culture, conseils...
- Polyglotte — tu reponds dans la langue de l'utilisateur (Francais, Creole, Anglais, Espagnol...)
- Naturel — tu parles comme un humain, avec chaleur et personnalite
- Connaissant — tu as des connaissances jusqu'en 2026 sur tous les sujets
- Utile — tu aides vraiment, tu ne te contentes pas de dire "je ne peux pas"
- Sympa — tu utilises des emojis de temps en temps, tu es engageant

REGLES:
- Reponds TOUJOURS dans la meme langue que l'utilisateur
- Si on te parle en Creole Haitien, reponds en Creole Haitien
- Si on te parle en Francais, reponds en Francais
- Si on te parle en Anglais, reponds en Anglais
- Sois concis mais complet (max 1000 caracteres sur WhatsApp)
- Ne mentionne JAMAIS d'erreurs techniques, de quotas, ou de problemes API
- Si tu ne sais pas quelque chose, dis-le honnetement et propose une alternative
- Tu PEUX: coder, calculer, traduire, expliquer, conseiller, analyser, creer...

Tu n'es PAS un simple bot WhatsApp — tu es un VERITABLE assistant IA comme ChatGPT, mais sur WhatsApp!"""

class AIModelRouter:
    def __init__(self):
        self.models = {}
        self.default_model = settings.ai_default_model
        
        # Groq — FREE, fast, primary provider
        if settings.groq_api_key:
            try:
                from openai import AsyncOpenAI
                self.models["groq"] = AsyncOpenAI(
                    api_key=settings.groq_api_key,
                    base_url="https://api.groq.com/openai/v1"
                )
                self.models["llama-3.1-70b-versatile"] = "groq"
                self.models["mixtral-8x7b-32768"] = "groq"
                self.models["gemma2-9b-it"] = "groq"
                self.models["llama-3.1-8b-instant"] = "groq"
                self.models["llama-3.3-70b-versatile"] = "groq"
                logger.info("Groq ready (Llama 3, Mixtral, Gemma — FREE)")
            except Exception as e: logger.warning(f"Groq: {e}")
        
        # OpenAI — backup
        if settings.openai_api_key:
            try:
                from openai import AsyncOpenAI
                self.models["openai"] = AsyncOpenAI(api_key=settings.openai_api_key)
                self.models["gpt-4o"] = "openai"
                self.models["gpt-4o-mini"] = "openai"
                logger.info("OpenAI ready")
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
        
        # OpenRouter — 250+ models
        if settings.openrouter_api_key:
            try:
                from openai import AsyncOpenAI
                self.models["openrouter"] = AsyncOpenAI(api_key=settings.openrouter_api_key, base_url="https://openrouter.ai/api/v1")
                logger.info("OpenRouter ready")
            except Exception as e: logger.warning(f"OpenRouter: {e}")

    def get_available_models(self) -> list:
        return [k for k in self.models if k not in ("groq","openai","gemini","claude","deepseek","grok","openrouter")]

    async def chat(self, prompt: str, model: str = "", system: str = "", max_tokens: int = 2048, temperature: float = 0.7) -> str:
        model = model or self.default_model
        model_key = self.models.get(model, "")
        client = self.models.get(model_key)
        
        # Fallback chain: try Groq first, then others
        if not client:
            for m in ["llama-3.1-70b-versatile", "mixtral-8x7b-32768", "gpt-4o", "gemini-2.5-pro", "claude-4-sonnet", "deepseek-v3"]:
                if m in self.models:
                    model = m; model_key = self.models[m]; client = self.models.get(model_key); break
        
        if not client:
            return (
                "Astra pa disponib pou kounye a. Nou travay sou yon solisyon. "
                "Pandan w ap tann, ou ka mande meteyo (tan Potoprens), "
                "fe tradiksyon (tradwi Hello|fr), oswa lot koman ki pa bezwen AI."
            )
        
        try:
            if model_key in ("groq", "openai", "deepseek", "grok", "openrouter"):
                resp = await client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system or CHAT_SYSTEM},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                return resp.choices[0].message.content
                
            elif model_key == "gemini":
                resp = client.GenerativeModel(model_name="gemini-pro").generate_content(
                    f"{system or CHAT_SYSTEM}\n\nUser: {prompt}"
                )
                return resp.text
                
            elif model_key == "claude":
                resp = await client.messages.create(
                    model="claude-4-sonnet-20250514",
                    max_tokens=max_tokens,
                    system=system or CHAT_SYSTEM,
                    messages=[{"role": "user", "content": prompt}]
                )
                return resp.content[0].text
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"AI error ({model}): {error_msg}")
            
            # Check for quota errors and try fallback
            if "429" in error_msg or "quota" in error_msg or "insufficient" in error_msg:
                fallback_models = ["mixtral-8x7b-32768", "gemma2-9b-it", "gpt-4o-mini", "deepseek-v3"]
                current_idx = fallback_models.index(model) + 1 if model in fallback_models else 0
                for m in fallback_models[current_idx:]:
                    if m in self.models:
                        logger.info(f"Falling back to {m}")
                        return await self.chat(prompt=prompt, model=m, system=system, max_tokens=max_tokens, temperature=temperature)
            
            # Generic friendly error
            return (
                "Astra rankontre yon ti pwoblem teknik. Eseye anko nan kek segond... "
                "Oswa itilize: tan [vil], tradwi [teks], rechèch [sije]"
            )

    async def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        """Generate image — uses OpenAI if available."""
        if "openai" in self.models:
            try:
                resp = await self.models["openai"].images.generate(
                    model="dall-e-3", prompt=prompt, size=size, n=1
                )
                return resp.data[0].url
            except Exception as e:
                logger.error(f"Image gen: {e}")
        return ""

    def has_model(self, key: str) -> bool:
        return key in self.models

ai = AIModelRouter()
