# 🏗 Astra Architecture

## Flow

WhatsApp User -> FastAPI (app/main.py)
  -> Webhook | REST API | Dashboard
  -> Intent Detector
  -> Chat AI | Media | Tools
  -> AI Model Router (GPT | Gemini | Claude | DeepSeek | Grok)
  -> WhatsApp Client

---

## Module Structure

```
app/
├── main.py          # FastAPI entry + all routes
├── config.py        # 40+ settings from .env
├── prompts.py       # AI system prompts
├── intents.py       # Intent detection (20+ patterns)
├── history.py       # Chat history
├── webhook.py       # WhatsApp webhook
├── whatsapp.py      # WhatsApp client
├── ai/              # 🤖 AI modules
│   ├── models.py    # Multi-model router
│   ├── chat.py      # Chat with context
│   ├── image.py     # Image generation
│   ├── video.py     # Video generation
│   ├── search.py    # Web search
│   ├── tts.py       # Text-to-speech
│   └── stt.py       # Speech-to-text
├── utils/           # 🔧 Utilities
│   ├── logger.py    # Logging
│   ├── helpers.py   # Helpers
│   ├── security.py  # Auth + rate limit
│   └── database.py  # Multi-DB support
├── github/          # 📂 GitHub integration
├── media/           # 🎨 Media generators
├── web/             # 🌐 Web services
├── programming/     # 💻 Code generation
├── files/           # 📄 File processing
├── deployment/      # ☁️ Deployment guides
└── dashboard/       # 📊 Admin dashboard
```
