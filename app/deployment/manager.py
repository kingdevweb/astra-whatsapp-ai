"""Deployment guides — Railway, Render, Docker, VPS, Replit."""
from app.utils.logger import logger

DEPLOY_GUIDES = {
    "railway": {"url": "https://railway.app", "steps": ["1. Push to GitHub", "2. Connect Railway to repo", "3. Set env vars", "4. Deploy"]},
    "render": {"url": "https://render.com", "steps": ["1. Push to GitHub", "2. New Web Service on Render", "3. Set build: pip install -r requirements.txt", "4. Set start: uvicorn app.main:app --host 0.0.0.0 --port $PORT"]},
    "docker": {"dockerfile": "FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD [\"uvicorn\",\"app.main:app\",\"--host\",\"0.0.0.0\",\"--port\",\"8000\"]"},
    "vps": {"steps": ["1. SSH into VPS", "2. git clone + pip install", "3. Use systemd or screen for uvicorn", "4. Set up nginx reverse proxy"]},
    "replit": {"url": "https://replit.com", "steps": ["1. Import from GitHub", "2. Add .replit file with run command", "3. Set secrets", "4. Run"]},
    "github_actions": {"steps": ["1. Push code", "2. .github/workflows/deploy.yml auto-deploys", "3. Set repo secrets for env vars"]},
}

async def get_deploy_guide(platform: str) -> dict:
    p = platform.lower()
    for k, v in DEPLOY_GUIDES.items():
        if k in p or p in k: return {"platform": k, **v}
    return {"platform": platform, "steps": ["Platform not found. Supported: railway, render, docker, vps, replit"]}
