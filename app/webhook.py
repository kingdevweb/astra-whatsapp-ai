"""Web and webhook handlers."""
from fastapi import APIRouter, Request, Query
from fastapi.responses import PlainTextResponse
from app.intents import detect_intent
from app.utils.logger import logger

router = APIRouter(prefix="/webhook", tags=["webhook"])

@router.get("")
async def verify(hub_mode: str = Query(None, alias="hub.mode"), hub_challenge: str = Query(None, alias="hub.challenge"), hub_verify_token: str = Query(None, alias="hub.verify_token")):
    from app.config import settings
    if hub_verify_token == settings.webhook_verify_token:
        return PlainTextResponse(hub_challenge or "ok")
    return PlainTextResponse("Forbidden", 403)

@router.post("")
async def receive(request: Request):
    try:
        body = await request.json()
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                for msg in change.get("value", {}).get("messages", []):
                    text = msg.get("text", {}).get("body", "")
                    if text:
                        intent = detect_intent(text)
                        return {"status": "received", "intent": intent}
        return {"status": "no_message"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
