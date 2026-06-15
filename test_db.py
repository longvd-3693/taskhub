import asyncio

from sqlalchemy import text

from app.core.database import SessionLocal


async def main():
    async with SessionLocal() as session:
        result = await session.execute(
            text("SELECT version()")
        )

        print(result.scalar())


asyncio.run(main())