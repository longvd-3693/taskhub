from app.models.enums import WorkspaceMemberRole
from app.repositories.workspace import WorkspaceRepository
from app.repositories.workspace_member import WorkspaceMemberRepository


class WorkspaceService:
    def __init__(
        self,
        repository: WorkspaceRepository,
        member_repository: WorkspaceMemberRepository,
    ):
        self.repository = repository
        self.member_repository = member_repository

    async def create_workspace(
        self,
        data: dict,
    ):
        workspace = await self.repository.create(data)

        await self.member_repository.create(
            {
                "workspace_id": workspace.id,
                "user_id": workspace.owner_id,
                "role": WorkspaceMemberRole.OWNER,
            }
        )

        return workspace

    async def get_workspace(
        self,
        workspace_id: int,
    ):
        return await self.repository.get_by_id(workspace_id)
