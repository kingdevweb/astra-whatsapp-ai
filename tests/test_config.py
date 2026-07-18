"""Test configuration."""
from app.config import Settings

def test_defaults():
    s = Settings()
    assert s.port == 8000
    assert s.host == "0.0.0.0"
    assert s.loglevel == "INFO"
    assert s.database_type == "sqlite"
    assert s.ai_default_model == "gpt-4o"
