from app.models.enums import ProjectStatus
from app.models.project import Project
from app.repositories.project import ProjectRepository


class ProjectService:

    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def create_project(
        self,
        workspace_id: int,
        data: dict,
    ):
        data["workspace_id"] = workspace_id
        data["status"] = ProjectStatus.ACTIVE

        return await self.repository.create(data)

    async def get_project(
        self,
        project_id: int,
    ):
        return await self.repository.get_by_id(project_id)

    async def get_project_with_workspace(
        self,
        project_id: int,
    ):
        return await self.repository.get_by_id_with_workspace(project_id)

    async def update_project(
        self,
        project: Project,
        data: dict,
    ):
        return await self.repository.update(project, data)

    async def archive_project(
        self,
        project: Project,
    ):
        return await self.repository.update(
            project,
            {
                "status": ProjectStatus.ARCHIVED,
            },
        )

    async def delete_project(
        self,
        project: Project,
    ):
        await self.repository.delete(project)
        return True