import json

from app.core.redis import redis_client


class CacheService:

    async def get(self, key: str):
        value = await redis_client.get(key)

        if value is None:
            return None

        return json.loads(value)

    async def set(
        self,
        key: str,
        value,
        expire_seconds: int = 60,
    ):
        await redis_client.set(
            key,
            json.dumps(value),
            ex=expire_seconds,
        )

    async def delete(self, key: str):
        await redis_client.delete(key)

    async def delete_by_pattern(self, pattern: str):
        cursor = 0

        while True:
            cursor, keys = await redis_client.scan(
                cursor=cursor,
                match=pattern,
            )

            if keys:
                await redis_client.delete(*keys)

            if cursor == 0:
                break