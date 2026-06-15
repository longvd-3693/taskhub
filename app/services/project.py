from app.repositories.project import ProjectRepository


class ProjectService:

    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def create_project(self, data: dict):
        return await self.repository.create(data)

    async def get_projects(self, page: int = 1, limit: int = 20):
        return await self.repository.paginate(page=page, limit=limit)

    async def get_project(self, project_id: int):
        return await self.repository.get_by_id(project_id)

    async def update_project(self, project_id: int, data: dict):
        project = await self.repository.get_by_id(project_id)
        if project is None:
            return None
        return await self.repository.update(project, data)

    async def delete_project(self, project_id: int):
        project = await self.repository.get_by_id(project_id)
        if project is None:
            return False
        await self.repository.delete(project)
        return True