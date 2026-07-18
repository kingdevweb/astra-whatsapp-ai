"""Chat history — in-memory store per user."""
from collections import defaultdict
from datetime import datetime

class ChatHistory:
    def __init__(self, max_per_user: int = 100):
        self._store: dict[str, list[dict]] = defaultdict(list)
        self._max = max_per_user

    def add(self, user_id: str, role: str, content: str):
        self._store[user_id].append({"role": role, "content": content, "timestamp": datetime.utcnow().isoformat()})
        if len(self._store[user_id]) > self._max:
            self._store[user_id] = self._store[user_id][-self._max:]

    def get(self, user_id: str, limit: int = 20) -> list[dict]:
        return self._store.get(user_id, [])[-limit:]

    def clear(self, user_id: str):
        self._store[user_id] = []

    def stats(self) -> dict:
        return {"total_users": len(self._store), "total_messages": sum(len(v) for v in self._store.values())}

history_store = ChatHistory()
