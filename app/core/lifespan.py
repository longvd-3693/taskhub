from contextlib import asynccontextmanager

from app.core.redis import close_redis



@asynccontextmanager
async def lifespan(app):
    print("🚀 TaskHub is starting...")

    yield

    print("🛑 TaskHub is shutting down...")
    await close_redis()