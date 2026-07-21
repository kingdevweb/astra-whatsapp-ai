"""Green API Webhook handlers for incoming WhatsApp messages."""
from fastapi import APIRouter, Request
from app.config import settings
from app.intents import detect_intent
from app.ai import chat as ai_chat
from app.ai import image as ai_image
from app.ai import search as ai_search
from app.ai import tts as ai_tts
from app.green_api import green_api
from app.web import news, weather, currency, translation
from app.files.processors import process_file
from app.utils.logger import logger
from app.utils.helpers import truncate

router = APIRouter(prefix="/webhook", tags=["webhook"])


def _extract_message(body: dict) -> dict | None:
    """Extract message details from Green API webhook payload."""
    try:
        instance_data = body.get("instanceData", {})
        sender_data = body.get("senderData", {})
        message_data = body.get("messageData", {})

        chat_id = sender_data.get("chatId", "")
        sender = sender_data.get("sender", "")
        sender_name = sender_data.get("senderName", "")

        msg_type = message_data.get("typeMessage", "")
        text = ""

        if msg_type == "textMessage":
            text = message_data.get("textMessageData", {}).get("textMessage", "")
        elif msg_type == "extendedTextMessage":
            text = message_data.get("extendedTextMessageData", {}).get("text", "")
        elif msg_type in ("imageMessage", "videoMessage"):
            caption = message_data.get(f"{msg_type.replace('Message','')}MessageData", {}).get("caption", "")
            file_url = message_data.get("downloadUrl", "")
            text = caption or "[media]"
        elif msg_type == "documentMessage":
            text = "[document]"
        elif msg_type == "audioMessage":
            text = "[audio]"

        return {
            "chat_id": chat_id,
            "sender": sender,
            "sender_name": sender_name,
            "text": text.strip(),
            "type": msg_type,
        }
    except Exception as e:
        logger.error(f"Failed to extract message: {e}")
        return None


async def _handle_message(msg: dict) -> str:
    """Process incoming message and return reply text."""
    text = msg.get("text", "")
    chat_id = msg.get("chat_id", "")

    if not text:
        return ""

    # Intent detection & routing
    intent = detect_intent(text)
    logger.info(f"Intent: {intent} | Text: {truncate(text, 100)}")

    if intent == "image":
        prompt = text.replace("imaj", "").replace("foto", "").replace("image", "").replace("jenere", "").strip()
        result = await ai_image.generate(prompt)
        img_url = result.get("url", "")
        if img_url:
            caption = result.get("prompt_used", prompt)[:500]
            await green_api.send_image(chat_id, img_url, caption)
            return f"✨ Men imaj ou: {caption}"
        return "⚠️ Jenere imaj bezwen OpenAI. Mwen ka ede w ake lòt bagay tou: eseye `rechèch [sijè]` oswa pale avè m!"

    elif intent == "search":
        query = text.replace("rechèch", "").replace("search", "").replace("google", "").strip()
        results = await ai_search.web_search(query)
        if results:
            reply = "🔍 *Rezilta rechèch:*\n\n"
            for i, r in enumerate(results[:5], 1):
                reply += f"{i}. *{r.get('title','')}*\n{r.get('snippet','')}\n\n"
            return reply
        return "Pa gen rezilta pou rechèch sa a."

    elif intent == "weather":
        city = text.replace("tan", "").replace("weather", "").replace("météo", "").strip()
        if not city:
            return "Tanpri bay non vil la. Egzanp: `tan Pòtoprens`"
        result = await weather.get_weather(city)
        if result.get("error"):
            return f"Pa t ka jwenn meteyo pou {city}."
        return (
            f"🌤 *Meteyo {result.get('city','')}*\n"
            f"🌡 Tanperati: {result.get('temp','')}°\n"
            f"💧 Imediti: {result.get('humidity','')}%\n"
            f"🌬 Van: {result.get('wind','')}\n"
            f"📋 {result.get('description','')}"
        )

    elif intent == "translate":
        parts = text.split("|")
        if len(parts) >= 2:
            txt = parts[0].strip()
            target = parts[1].strip()
        else:
            txt = text.replace("tradwi", "").replace("translate", "").strip()
            target = "en"
        result = await translation.translate_text(txt, target)
        return f"🌐 *Tradiksyon:*\n\n{result.get('translated','')}"

    elif intent == "currency":
        return await currency.get_rates()

    elif intent == "news":
        return await news.get_headlines()

    elif intent == "tts":
        tts_text = text.replace("vwa", "").replace("tts", "").replace("pale", "").strip()
        if tts_text:
            result = await ai_tts.text_to_speech(tts_text)
            audio_url = result.get("url", "")
            if audio_url:
                await green_api.send_audio(chat_id, audio_url)
                return f"🔊 {tts_text[:100]}"
        return "Tanpri bay tèks pou m pale."

    elif intent == "help":
        return (
            "🤖 *Astra — Asistan AI sou WhatsApp*\n\n"
            "💫 *Chat GPT-Style* — pale avè m pou nenpòt kesyon!\n"
            "🖼 *Imaj* — `foto [deskripsyon]`\n"
            "🔍 *Rechèch* — `rechèch [sijè]`\n"
            "🌤 *Meteyo* — `tan [vil]`\n"
            "🌐 *Tradiksyon* — `tradwi [tèks]|[lang]`\n"
            "💰 *Lajan* — `to lajan`\n"
            "📰 *Nouvèl* — `nouvèl`\n"
            "🗣 *Vwa* — `vwa [tèks]`\n\n"
            "✨ *www.astra-ai.com)"
        )

    else:
        # Default: AI Chat (like ChatGPT!)
        reply = await ai_chat.chat_reply(text, chat_id)
        if reply:
            return truncate(reply, 4000)
        return "🤖 Désolé, je n'arrive pas à traiter ta demande. Reessaie!"


@router.get("")
async def health_check():
    """Simple health endpoint for webhook testing."""
    return {"status": "ok", "service": "Astra WhatsApp AI + Groq"}


@router.post("")
async def receive(request: Request):
    """Receive incoming webhook notifications from Green API."""
    try:
        raw_body = await request.json()
        webhook_body = raw_body.get("body", raw_body)
        webhook_type = webhook_body.get("typeWebhook", "")

        logger.info(f"Webhook received: {webhook_type}")

        if webhook_type in ("incomingMessageReceived", "incomingMessage"):
            msg = _extract_message(webhook_body)
            if msg and msg.get("text"):
                reply = await _handle_message(msg)
                if reply:
                    await green_api.send_message(msg["chat_id"], reply)
                    logger.info(f"Replied to {msg['sender_name']}: {truncate(reply, 60)}")

        return {"status": "received"}

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"status": "error", "message": str(e)}
