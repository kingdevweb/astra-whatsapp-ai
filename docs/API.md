# 📡 Astra API Reference

Base URL: `http://localhost:8000`

## Chat
`POST /chat` — AI chat with multi-model support
```json
{"message": "Hello", "user_id": "123", "model": "gpt-4o"}
```

## Image
`POST /image/generate` — Generate AI images
```json
{"prompt": "a sunset", "style": "realistic"}
```

## Search
`GET /search?q=python` — Web search  
`GET /search?q=tech&news_search=true` — News

## Weather
`GET /weather/port-au-prince` — Free, no API key

## Currency
`GET /currency/convert?amount=100&from_cur=USD&to_cur=HTG`

## Translation
`POST /translate` — 100+ languages
```json
{"text": "Hello world", "target": "ht"}
```

## TTS
`POST /tts — Text to speech
```json
{"text": "Hello", "voice": "alloy"}
```

## Sticker / Logo / Banner / Avatar
`POST /sticker` `POST /logo` `POST /banner` `POST /avatar`

## GitHub
`GET /github/repo/{owner}/{repo}?path=README.md`  
`POST /github/commit` `POST /github/pr` `POST /github/issue`

## Code Generation
`POST /code/generate` `POST /code/debug` `POST /code/explain`  
`POST /code/apk` `POST /code/api` `POST /code/website`

## File Processing
`POST /file/process` — PDF, Word, Excel, JSON, CSV
```json
{"path": "/path/to/file.pdf"}
```

## Deploy
`GET /deploy/{platform}` — railway, render, docker, vps, replit

## Dashboard (requires JWT)
`POST /dashboard/login`  
`GET /dashboard/stats` `GET /dashboard/health`

## Intent Detection
`POST /intent`
```json
{"message": "generate a logo"}
```

## Broadcast
`POST /broadcast`
```json
{"contacts": ["+50912345678"], "text": "Hello everyone!"}
```
