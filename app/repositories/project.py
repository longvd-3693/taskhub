from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.project import Project
from app.models.workspace import Workspace
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Project)

    async def get_by_id_with_workspace(
        self,
        project_id: int,
    ) -> Project | None:
        result = await self.session.execute(
            select(Project)
            .options(selectinload(Project.workspace).selectinload(Workspace.members))
            .where(Project.id == project_id)
        )

        return result.scalar_one_or_none()
