# ☁️ Deployment Guide

## Railway (Recommended)
1. Push to GitHub
2. [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add environment variables from `.env.example`
4. Deploy!

## Render
1. Push to GitHub
2. [render.com](https://render.com) → New Web Service
3. Build: `pip install -r requirements.txt`
4. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Docker
```bash
docker build -t astra-whatsapp-ai .
docker run -p 8000:8000 --env-file .env astra-whatsapp-ai
```

Dockerfile:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
```

## VPS (Ubuntu)
```bash
sudo apt update && sudo apt install python3-pip nginx -y
git clone https://github.com/kingdevweb/astra-whatsapp-ai.git
cd astra-whatsapp-ai && pip install -r requirements.txt
cp .env.example .env  # edit with your keys
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Replit
Import from GitHub → Add `.replit`:
```
run = "uvicorn app.main:app --host 0.0.0.0 --port 8000"
```

## GitHub Actions
Auto-deploy via `.github/workflows/deploy.yml`
