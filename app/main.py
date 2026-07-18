"""Astra WhatsApp AI — Ultra Premium | Main Entry Point."""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.utils.logger import logger
from app.whatsapp import whatsapp
from app.webhook import router as webhook_router
from app.dashboard.api import router as dashboard_router
from app.intents import detect_intent
from app.ai import chat as ai_chat
from app.ai import image as ai_image
from app.ai import search as ai_search
from app.ai import tts as ai_tts
from app.ai import stt as ai_stt
from app.media import sticker, logo, banner, avatar
from app.web import news, weather, currency, translation
from app.programming import generator, apk, api as prog_api, website
from app.github.client import github_client
from app.files.processors import process_file
from app.deployment.manager import get_deploy_guide
from app.utils.security import check_rate_limit
from app.utils.helpers import truncate

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("😀 Astra WhatsApp AI — Ultra Premium v2.0")
    try:
        await whatsapp.start()
    except:
        pass
    yield
    await whatsapp.stop()

app = FastAPI(title="Astra WhatsApp AI", version="2.0.0-ultra", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(webhook_router)
if settings.dashboard_enabled: app.include_router(dashboard_router)

@app.get("/")
async def root(): return {"name":"Astra WhatsApp AI","version":"2.0.0-ultra","status":"running"}

@app.get("/health")
async def health(): return {"status":"ok"}

@app.post("/chat")
async def chat_endpoint(request: Request):
    body = await request.json()
    reply = await ai_chat.chat_reply(body.get("message",""), body.get("user_id","api"), body.get("model",""))
    return {"reply": reply}

@app.post("/image/generate")
async def image_generate(request: Request):
    body = await request.json()
    result = await ai_image.generate(body.get("prompt",""), body.get("style","realistic"))
    return result

@app.get("/search")
async def search_endpoint(q: str = ""): return await ai_search.web_search(q)

@app.get("/weather/{city}")
async def weather_endpoint(city: str): return await weather.get_weather(city)

@app.get("/currency/convert")
async def currency_endpoint(amount: float, from_cur: str, to_cur: str): return await currency.convert(amount, from_cur, to_cur)

@app.post("/translate")
async def translate_endpoint(request: Request):
    body = await request.json()
    return await translation.translate_text(body.get("text",""), body.get("target","en"), body.get("source","auto"))

@app.post("/tts")
async def tts_endpoint(request: Request):
    body = await request.json()
    return await ai_tts.text_to_speech(body.get("text",""), body.get("voice","alloy"))

@app.post("/logo")
async def logo_endpoint(request: Request):
    body = await request.json()
    return await logo.generate_logo(body.get("name",""), body.get("industry","tech"), body.get("style","minimal"))

@app.post("/code/generate")
async def code_gen(request: Request):
    body = await request.json()
    return {"code": await generator.generate_code(body.get("spec",""), body.get("language","python"), body.get("framework",""))}

@app.get("/deploy/{platform}")
async def deploy_guide(platform: str): return await get_deploy_guide(platform)

@app.post("/intent")
async def intent_endpoint(request: Request):
    body = await request.json()
    return {"intent": detect_intent(body.get("message",""))}

def run():
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)

if __name__ == "__main__:": run()
