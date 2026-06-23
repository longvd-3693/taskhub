import logging
import asyncio

from sqlalchemy import text

from app.core.logging import configure_logging
from app.core.database import SessionLocal


configure_logging()
logger = logging.getLogger(__name__)


async def main():
    async with SessionLocal() as session:
        result = await session.execute(
            text("SELECT version()")
        )

        logger.info(
            "Database version fetched",
            extra={"database_version": result.scalar()},
        )


asyncio.run(main())