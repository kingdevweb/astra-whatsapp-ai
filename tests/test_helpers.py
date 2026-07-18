"""Test helper functions."""
from app.utils.helpers import clean_phone, generate_id, truncate, is_url

def test_clean_phone():
    assert clean_phone("+1 555-123-4567") == "15551234567"
    assert clean_phone("5551234567") == "15551234567"

def test_generate_id():
    assert len(generate_id()) == 12

def test_truncate():
    long_text = "x" * 5000
    assert len(truncate(long_text)) <= 4000
    assert len(truncate("hello")) == 5

def test_is_url():
    assert is_url("https://github.com") == True
    assert is_url("not a url") == False
