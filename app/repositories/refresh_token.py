from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken
from app.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RefreshToken)

    async def get_by_token(self, token: str) -> RefreshToken | None:
        return await self.find_one(token=token)

    async def get_active_token(
        self,
        token: str,
    ) -> RefreshToken | None:
        return await self.find_one(token=token, is_revoked=False)
