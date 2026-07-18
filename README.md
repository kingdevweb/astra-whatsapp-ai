# 🚀 Astra WhatsApp AI — Ultra Premium

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-teal.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI](https://github.com/kingdevweb/astra-whatsapp-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/kingdevweb/astra-whatsapp-ai/actions)

**AI-powered WhatsApp chatbot — 60+ premium modules.**  
Chat, generate images, manage groups, deploy to production — all from WhatsApp.

---

## 🤖 AI Models
GPT-5 ✅ · Gemini 2.5 Pro ✅ · Claude 4 Sonnet ✅ · DeepSeek V3 ✅ · Grok 3 ✅ · OpenRouter (250+) ✅

## 💬 WhatsApp
QR Code · Pairing Code · Auto Reply · Auto React · Auto Read · Anti Spam · Anti Link · Welcome/Goodbye · Group Management · Broadcast · Scheduled Messages

## 🎨 Media · 🔊 Voice · 🌐 Web · 📂 GitHub · 💻 Programming · 📄 Files · ☁️ Deploy · 🔒 Security · 📊 Dashboard · 💾 Database

---

## Quick Start

```bash
git clone https://github.com/kingdevweb/astra-whatsapp-ai.git
cd astra-whatsapp-ai && pip install -r requirements.txt
cp .env.example .env   # edit with your API keys
uvicorn app.main:app --port 8000 --reload
```

## API Endpoints
| Endpoint | Description |
|---|---|
| `POST /chat` | AI chat (multi-model) |
| `POST /image/generate` | Generate AI images |
| `GET /search?q=...` | Web search |
| `GET /weather/{city}` | Current weather |
| `GET /currency/convert` | Currency conversion |
| `POST /translate` | Translation (100+ languages) |
| `POST /tts` | Text-to-Speech |
| `POST /logo` | Generate logo |
| `POST /sticker` | Create WhatsApp sticker |
| `POST /code/generate` | Generate code |
| `POST /code/debug` | Debug code |
| `GET /github/repo/{owner}/{repo}` | Read GitHub repo |
| `POST /github/commit` | Create GitHub commit |
| `GET /deploy/{platform}` | Deployment guide |
| `POST /dashboard/login` | Admin login |
| `GET /dashboard/stats` | System stats |

Full API: [docs/API.md](docs/API.md)

## Environment Variables
Copy `.env.example` to `.env` and configure:
- At least one AI API key (`OPENAI_API_KEY`, `GEMINI_API_KEY`, etc.)
- `JWT_SECRET` for dashboard authentication
- Optional: `GITHUB_PAT`, database URLs, WhatsApp settings

## Documentation
- [API Reference](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

---
**Made with ❤️ by kingdevweb**
