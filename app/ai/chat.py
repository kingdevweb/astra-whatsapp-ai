"""AI chat with context."""
from app.ai.models import ai
from app.prompts import SYSTEM_PROMPT
from app.history import history_store

async def chat_reply(user_message: str, user_id: str = "default", model: str = "", system_prompt: str = "") -> str:
    recent = history_store.get(user_id, limit=10)
    ctx = "\n".join([f"{'User' if m['role']=='user' else 'Astra'}: {m['content']}" for m in recent])
    full = f"Previous:\n{ctx}\n\nUser: {user_message}" if ctx else user_message
    reply = await ai.chat(prompt=full, model=model, system=system_prompt or SYSTEM_PROMPT)
    history_store.add(user_id, "user", user_message); history_store.add(user_id, "assistant", reply)
    return reply
