from app.repositories.workspace import WorkspaceRepository


class WorkspaceService:

    def __init__(self, repository: WorkspaceRepository):
        self.repository = repository

    async def create_workspace(self, data: dict):
        return await self.repository.create(data)

    async def get_workspaces(self, page: int = 1, limit: int = 20):
        return await self.repository.paginate(page=page, limit=limit)

    async def get_workspace(self, workspace_id: int):
        return await self.repository.get_by_id(workspace_id)

    async def update_workspace(self, workspace_id: int, data: dict):
        workspace = await self.repository.get_by_id(workspace_id)

        if workspace is None:
            return None

        return await self.repository.update(workspace, data)

    async def delete_workspace(self, workspace_id: int):
        workspace = await self.repository.get_by_id(workspace_id)

        if workspace is None:
            return False

        await self.repository.delete(workspace)
        return True