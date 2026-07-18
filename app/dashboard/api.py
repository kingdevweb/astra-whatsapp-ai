"""Dashboard API."""
from fastapi import APIRouter, Depends
from app.utils.security import require_admin, create_jwt, verify_admin
from app.history import history_store
from app.ai.models import ai
from pydantic import BaseModel

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

class LoginRequest(BaseModel): username: str; password: str

class LoginResponse(BaseModel): token: str; user: str

@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest):
    if not verify_admin(req.username, req.password):
        from fastapi import HTTPException; raise HTTPException(401, "Invalid credentials")
    return {"token": create_jwt({"user": req.username, "is_admin": True}), "user": req.username}

@router.get("/stats")
async def stats(_ = Depends(require_admin)):
    return {"chat": history_store.stats(), "ai_models": ai.get_available_models(), "default_model": __import__("app.config", fromlist=["settings"]).settings.ai_default_model}
