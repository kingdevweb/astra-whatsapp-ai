"""WhatsApp Web client — QR/Pairing auth, messaging, group management."""
import os, asyncio
from typing import Callable, Optional
from app.config import settings
from app.utils.logger import logger

class WhatsAppClient:
    def __init__(self):
        self.client = None
        self.is_connected = False
        self.qr_callback: Optional[Callable] = None
        self.message_callback: Optional[Callable] = None

    async def start(self, qr_callback: Callable = None, msg_callback: Callable = None):
        self.qr_callback = qr_callback
        self.message_callback = msg_callback
        os.makedirs(settings.whatsapp_session_dir, exist_ok=True)
        logger.info(f"Starting WhatsApp (auth: {settings.whatsapp_auth_type})")
        try:
            from whatsapp_web_py import Client, LocalAuth
            self.client = Client(auth_strategy=LocalAuth(data_path=settings.whatsapp_session_dir), puppeteer_args=["--no-sandbox","--disable-setuid-sandbox"])
            self.client.on("qr", lambda qr: self.qr_callback(qr) if self.qr_callback else None)
            self.client.on("ready", self._on_ready)
            self.client.on("message", self._on_message)
            self.client.on("disconnected", self._on_disconnected)
            self.client.initialize()
        except ImportError:
            logger.warning("whatsapp-web-py not installed — mock mode")
            self.is_connected = True

    def _on_ready(self): self.is_connected = True; logger.info("WhatsApp ready!")

    async def _on_message(self, message):
        if self.message_callback: await self.message_callback(message)

    def _on_disconnected(self, reason): self.is_connected = False; logger.warning(f"Disconnected: {reason}")

    async def send_message(self, to: str, text: str) -> bool:
        try:
            if self.client: await self.client.send_message(to, text); return True
        except Exception as e: logger.error(f"Send failed: {e}")
        return False

    async def send_image(self, to: str, image_path: str, caption: str = "") -> bool:
        try:
            if self.client:
                from whatsapp_web_py import MessageMedia
                await self.client.send_message(to, MessageMedia.from_file(image_path), caption=caption); return True
        except Exception as e: logger.error(f"Image send failed: {e}")
        return False

    async def send_reaction(self, message_id: str, emoji: str = "👍") -> bool:
        try:
            if self.client: await self.client.react(message_id, emoji); return True
        except Exception as e: logger.error(f"Reaction failed: {e}")
        return False

    async def mark_read(self, chat_id: str) -> bool:
        try:
            if self.client: await self.client.send_seen(chat_id); return True
        except Exception as e: logger.error(f"Mark read failed: {e}")
        return False

    async def broadcast(self, contacts: list, text: str) -> dict:
        results = {"sent": 0, "failed": 0}
        for c in contacts:
            if await self.send_message(c, text): results["sent"] += 1
            else: results["failed"] += 1
        return results

    async def stop(self):
        if self.client:
            try: await self.client.destroy()
            except: pass
        self.is_connected = False

whatsapp = WhatsAppClient()
