import logging
from contextlib import asynccontextmanager

from app.core.logging import configure_logging
from app.core.redis import close_redis


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    configure_logging()
    logger.info("TaskHub application started")

    yield

    logger.info("TaskHub application stopped")
    await close_redis()