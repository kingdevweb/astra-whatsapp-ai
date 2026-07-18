"""Auth & rate limiting."""
import time, hmac
from collections import defaultdict
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer
from app.config import settings

security = HTTPBearer(auto_error=False)
rate_windows: dict[str, list[float]] = defaultdict(list)

def create_jwt(payload: dict, expires_in: int = 3600) -> str:
    from jose import jwt
    payload["exp"] = int(time.time()) + expires_in; payload["iat"] = int(time.time())
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

def verify_jwt(token: str) -> dict:
    from jose import jwt, JWTError
    try: return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    except JWTError: raise HTTPException(401, "Invalid token")

def verify_admin(username: str, password: str) -> bool:
    return hmac.compare_digest(username, settings.admin_username) and hmac.compare_digest(password, settings.admin_password)

async def require_admin(credentials = Depends(security)) -> dict:
    if not credentials: raise HTTPException(401, "Auth required")
    p = verify_jwt(credentials.credentials)
    if not p.get("is_admin"): raise HTTPException(403, "Admin only")
    return p

def check_rate_limit(request: Request) -> bool:
    if not settings.rate_limit_enabled: return True
    key = request.client.host if request.client else "unknown"
    now = time.time()
    rate_windows[key] = [t for t in rate_windows[key] if now - t < 60]
    if len(rate_windows[key]) >= settings.rate_limit_per_minute:
        raise HTTPException(429, "Rate limit exceeded")
    rate_windows[key].append(now)
    return True
