from typing import Generic, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def create(self, data: dict) -> T:
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(self, id: int) -> T | None:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[T]:
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def paginate(self, page: int = 1, limit: int = 20) -> list[T]:
        if page < 1:
            raise ValueError("page must be >= 1")
        if limit < 1:
            raise ValueError("limit must be >= 1")

        offset = (page - 1) * limit

        result = await self.session.execute(
            select(self.model).order_by(self.model.id).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar_one()

    async def exists(self, id: int) -> bool:
        return await self.get_by_id(id) is not None

    async def find_one(self, **filters) -> T | None:
        result = await self.session.execute(select(self.model).filter_by(**filters))
        return result.scalar_one_or_none()

    async def update(self, obj: T, data: dict) -> T:
        for key, value in data.items():
            setattr(obj, key, value)

        await self.session.commit()
        await self.session.refresh(obj)

        return obj

    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)
        await self.session.commit()
