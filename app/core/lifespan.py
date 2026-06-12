from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app):
    print("🚀 TaskHub is starting...")

    yield

    print("🛑 TaskHub is shutting down...")