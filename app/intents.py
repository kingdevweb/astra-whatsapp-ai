"""Intent detection for routing messages."""
import re

INTENT_PATTERNS = {
    "image_generate": [r"\b(generate|create|draw|make)\b.*\b(image|picture|photo|art)\b"],
    "image_edit": [r"\b(edit|modify|enhance|retouch)\b.*\b(image|picture|photo)\b"],
    "video_generate": [r"\b(generate|create|make)\b.*\b(video|clip|animation)\b"],
    "voice_transcribe": [r"\b(transcribe|speech.to.text|listen to)\b"],
    "tts": [r"\b(speak|say|read aloud|text.to.speech)\b"],
    "weather": [r"\b(weather|temperature|forecast|climate|rain|sunny)\b"],
    "web_search": [r"\b(search|google|look up|find)\b.*\b(online|web|internet)\b", r"\b(what is|who is|how to|where is|when did)\b"],
    "news": [r"\b(news|headlines|latest|breaking|trending)\b"],
    "currency": [r"\b(convert|exchange|rate)\b.*\b(usd|eur|htg|dollar|gourde|currency)\b"],
    "translation": [r"\b(translate|translation)\b", r"\b(say|how do you say)\b.*\b(in|into)\b"],
    "github": [r"\b(github|repo|repository|commit|push|pull request|issue|release)\b"],
    "code_generate": [r"\b(write|generate|create|code|build)\b.*\b(code|script|function|program|app|api|bot)\b"],
    "code_debug": [r"\b(debug|fix|error|bug|not working)\b"],
    "code_explain": [r"\b(explain|what does|how does)\b.*\b(code|function|script)\b"],
    "sticker": [r"\b(sticker)\b"],
    "logo": [r"\b(create|make|design|generate)\b.*\b(logo|icon|brand)\b", r"\b(logo|icon|brand)\b.*\b(create|make|design|generate)\b"],
    "banner": [r"\b(banner|flyer|poster)\b"],
    "deploy": [r"\b(deploy|host|launch|publish)\b.*\b(render|railway|replit|docker|vps|server)\b"],
    "scheduled_message": [r"\b(schedule|remind|delay|send.*later)\b.*\b(message|text)\b"],
    "broadcast": [r"\b(broadcast|announce|send to all|mass message)\b"],
}

def detect_intent(message: str) -> str:
    msg = message.lower().strip()
    scores = {}
    for intent, patterns in INTENT_PATTERNS.items():
        score = sum(1 for p in patterns if re.search(p, msg))
        if score > 0:
            scores[intent] = score
    if not scores:
        return "chat"
    # If weather is matched and there's no explicit search keyword, prefer weather
    if "weather" in scores and "web_search" in scores:
        # Check if there's an explicit search keyword (not just "what is")
        if scores["weather"] >= scores["web_search"]:
            del scores["web_search"]
    return max(scores, key=scores.get)

def get_all_intents(message: str) -> list:
    msg = message.lower().strip()
    scores = {intent: sum(1 for p in patterns if re.search(p, msg)) for intent, patterns in INTENT_PATTERNS.items()}
    return sorted([k for k, v in scores.items() if v > 0], key=lambda k: scores[k], reverse=True)
