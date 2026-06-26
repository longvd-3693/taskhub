from app.repositories.user import UserRepository
from app.auth.hashing import hash_password


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, data: dict):
        data["hashed_password"] = hash_password(data.pop("password"))
        return await self.repository.create(data)

    async def get_users(self, page: int = 1, limit: int = 20):
        return await self.repository.paginate(page=page, limit=limit)

    async def get_user(self, user_id: int):
        return await self.repository.get_by_id(user_id)

    async def update_user(self, user_id: int, data: dict):
        user = await self.repository.get_by_id(user_id)

        if user is None:
            return None

        return await self.repository.update(user, data)

    async def delete_user(self, user_id: int):
        user = await self.repository.get_by_id(user_id)

        if user is None:
            return False

        await self.repository.delete(user)

        return True
