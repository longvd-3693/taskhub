from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.project import Project
from app.models.task import Task
from app.repositories.base import BaseRepository
from app.models.workspace import Workspace


class TaskRepository(BaseRepository[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Task)

    async def get_by_id_with_project_workspace(
        self,
        task_id: int,
    ) -> Task | None:
        result = await self.session.execute(
            select(Task)
            .options(
                selectinload(Task.project)
                .selectinload(Project.workspace)
                .selectinload(Workspace.members)
            )
            .where(Task.id == task_id)
        )
        return result.scalar_one_or_none()

    async def get_by_project(
        self,
        project_id: int,
        page: int = 1,
        limit: int = 20,
    ) -> list[Task]:
        offset = (page - 1) * limit

        result = await self.session.execute(
            select(Task)
            .where(Task.project_id == project_id)
            .order_by(Task.id)
            .offset(offset)
            .limit(limit)
        )

        return list(result.scalars().all())
