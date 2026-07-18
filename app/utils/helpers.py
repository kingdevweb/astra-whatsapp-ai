"""Helper functions."""
import re, hashlib, uuid
from datetime import datetime, timezone

def clean_phone(phone: str) -> str:
    d = re.sub(r"\D", "", phone)
    return "1" + d if not d.startswith("1") and len(d) == 10 else d

def generate_id() -> str: return uuid.uuid4().hex[:12]
def hash_text(text: str) -> str: return hashlib.sha256(text.encode()).hexdigest()[:16]
def now_iso() -> str: return datetime.now(timezone.utc).isoformat()

def truncate(text: str, max_len: int = 4000) -> str:
    return text if len(text) <= max_len else text[:max_len - 50] + "\n\n... [truncated]"

def extract_code_blocks(text: str) -> list:
    return re.findall(r"```[\s\S]*?```", text)

def is_url(text: str) -> bool: return bool(re.match(r"https?://[^\s]+", text))
