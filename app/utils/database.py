"""Multi-DB — SQLite, PostgreSQL, MySQL, MongoDB, Redis."""
from app.config import settings
from app.utils.logger import logger

class DatabaseManager:
    def __init__(self): self._engine = None; self._redis = None; self._mongo = None

    async def initialize(self):
        db = settings.database_type; logger.info(f"DB: {db}")
        try:
            if db == "sqlite":
                from sqlalchemy.ext.asyncio import create_async_engine
                self._engine = create_async_engine(settings.database_url.replace("sqlite:///","sqlite+aiosqlite:///"), echo=False)
            elif db == "postgresql":
                from sqlalchemy.ext.asyncio import create_async_engine
                self._engine = create_async_engine(settings.postgres_url, echo=False)
            elif db == "mysql":
                from sqlalchemy.ext.asyncio import create_async_engine
                self._engine = create_async_engine(settings.mysql_url, echo=False)
            elif db == "mongodb":
                from pymongo import AsyncMongoClient
                self._mongo = AsyncMongoClient(settings.mongodb_url)
            logger.info(f"✅ {db} connected")
        except Exception as e: logger.warning(f"{db}: {e}")
        if settings.redis_url:
            try:
                import redis.asyncio as aioredis
                self._redis = aioredis.from_url(settings.redis_url); await self._redis.ping()
                logger.info("✅ Redis connected")
            except Exception as e: logger.warning(f"Redis: {e}")

    async def health(self) -> dict:
        s = {"db": settings.database_type, "connected": self._engine is not None}
        if self._redis:
            try: await self._redis.ping(); s["redis"] = "ok"
            except: s["redis"] = "down"
        return s

db = DatabaseManager()
