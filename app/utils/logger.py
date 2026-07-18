"""Structured logging."""
import logging, sys
from app.config import settings

def setup_logger(name: str = "astra") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.loglevel.upper(), logging.INFO))
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)s | %(message)s", "%Y-%m-%d %H:%M:%S"))
        logger.addHandler(h)
    return logger

logger = setup_logger("astra")
