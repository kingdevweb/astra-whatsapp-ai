"""Green API WhatsApp Business Client — REST-based messaging."""
import httpx
import base64
from typing import Optional
from app.config import settings
from app.utils.logger import logger


class GreenAPIClient:
    """Green API client for sending/receiving WhatsApp messages."""

    def __init__(self):
        self.id_instance: str = settings.green_api_id_instance
        self.token_instance: str = settings.green_api_token_instance
        self.api_url: str = settings.green_api_url.rstrip("/")
        self.is_connected: bool = False
        self.phone: str = settings.green_api_phone

    @property
    def _base_url(self) -> str:
        return f"{self.api_url}/waInstance{self.id_instance}"

    async def check_status(self) -> bool:
        """Verify the instance is authorized."""
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(
                    f"{self._base_url}/getStateInstance/{self.token_instance}",
                )
                data = resp.json()
                self.is_connected = data.get("stateInstance") == "authorized"
                if self.is_connected:
                    logger.info("Green API instance authorized ✅")
                else:
                    logger.warning(f"Green API status: {data.get('stateInstance')}")
                return self.is_connected
        except Exception as e:
            logger.error(f"Green API status check failed: {e}")
            return False

    async def send_message(self, to: str, text: str) -> bool:
        """Send a text message. `to` can be phone number or chatId."""
        chat_id = self._normalize_chat_id(to)
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.post(
                    f"{self._base_url}/sendMessage/{self.token_instance}",
                    json={"chatId": chat_id, "message": text},
                )
                data = resp.json()
                if resp.status_code == 200:
                    logger.info(f"Message sent to {chat_id}: {text[:50]}...")
                    return True
                else:
                    logger.error(f"Send failed: {data}")
                    return False
        except Exception as e:
            logger.error(f"Green API send error: {e}")
            return False

    async def send_image(self, to: str, image_url: str, caption: str = "") -> bool:
        """Send an image via URL."""
        chat_id = self._normalize_chat_id(to)
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    f"{self._base_url}/sendFileByUrl/{self.token_instance}",
                    json={
                        "chatId": chat_id,
                        "urlFile": image_url,
                        "fileName": "image.jpg",
                        "caption": caption,
                    },
                )
                data = resp.json()
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Green API image send error: {e}")
            return False

    async def send_document(self, to: str, doc_url: str, filename: str = "file.pdf") -> bool:
        """Send a document via URL."""
        chat_id = self._normalize_chat_id(to)
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    f"{self._base_url}/sendFileByUrl/{self.token_instance}",
                    json={
                        "chatId": chat_id,
                        "urlFile": doc_url,
                        "fileName": filename,
                    },
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Green API document send error: {e}")
            return False

    async def send_audio(self, to: str, audio_url: str) -> bool:
        """Send an audio/voice note via URL."""
        chat_id = self._normalize_chat_id(to)
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(
                    f"{self._base_url}/sendFileByUrl/{self.token_instance}",
                    json={
                        "chatId": chat_id,
                        "urlFile": audio_url,
                        "fileName": "audio.ogg",
                    },
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Green API audio send error: {e}")
            return False

    async def broadcast(self, contacts: list, text: str) -> dict:
        """Broadcast a message to multiple contacts."""
        results = {"sent": 0, "failed": 0}
        for contact in contacts:
            if await self.send_message(contact, text):
                results["sent"] += 1
            else:
                results["failed"] += 1
        return results

    async def set_webhook(self, webhook_url: str) -> bool:
        """Configure the webhook URL for incoming messages."""
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.post(
                    f"{self._base_url}/setSettings/{self.token_instance}",
                    json={"webhookUrl": webhook_url},
                )
                return resp.status_code == 200
        except Exception as e:
            logger.error(f"Webhook setup failed: {e}")
            return False

    def _normalize_chat_id(self, to: str) -> str:
        """Normalize phone numbers to Green API chatId format."""
        to = to.strip().replace("+", "").replace(" ", "").replace("-", "")
        if "@c.us" not in to and "@g.us" not in to:
            to = f"{to}@c.us"
        return to


green_api = GreenAPIClient()
