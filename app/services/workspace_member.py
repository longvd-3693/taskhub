from app.models.enums import WorkspaceMemberRole
from app.repositories.workspace_member import WorkspaceMemberRepository


class WorkspaceMemberService:

    def __init__(
        self,
        repository: WorkspaceMemberRepository,
    ):
        self.repository = repository

    async def add_member(
        self,
        workspace_id: int,
        user_id: int,
        role: WorkspaceMemberRole,
    ):
        existing_member = await self.repository.get_member(
            workspace_id,
            user_id,
        )

        if existing_member is not None:
            return None

        return await self.repository.create(
            {
                "workspace_id": workspace_id,
                "user_id": user_id,
                "role": role,
            }
        )

    async def remove_member(
        self,
        workspace_id: int,
        user_id: int,
    ) -> bool:
        member = await self.repository.get_member(
            workspace_id,
            user_id,
        )

        if member is None:
            return False

        if member.role == WorkspaceMemberRole.OWNER:
            return False

        await self.repository.delete(member)
        return True