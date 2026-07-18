"""Test intent detection."""
from app.intents import detect_intent, get_all_intents

def test_chat():
    assert detect_intent("Hello how are you?") == "chat"

def test_image_generate():
    assert detect_intent("generate a picture of a sunset") == "image_generate"

def test_weather():
    assert detect_intent("what is the weather in port-au-prince") == "weather"

def test_translation():
    assert detect_intent("translate hello to french") == "translation"

def test_code_generate():
    assert detect_intent("write a python script to sort a list") == "code_generate"

def test_github():
    assert detect_intent("read my github repo kingdevweb/test") == "github"

def test_news():
    assert detect_intent("latest news about technology") == "news"

def test_currency():
    assert detect_intent("convert 100 usd to htg") == "currency"

def test_logo():
    assert detect_intent("create a logo for my business") == "logo"

def test_all_intents():
    intents = get_all_intents("generate an image of a cat and translate cat to spanish")
    assert len(intents) >= 2
    assert "image_generate" in intents
    assert "translation" in intents
