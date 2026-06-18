from fastapi import Depends, HTTPException, status

from app.auth.dependencies import get_current_active_user
from app.dependencies import get_workspace_member_service, get_workspace_service
from app.models.enums import WorkspaceMemberRole
from app.models.user import User
from app.models.workspace import Workspace
from app.services.workspace import WorkspaceService
from app.services.workspace_member import WorkspaceMemberService


async def require_workspace_owner(
    workspace_id: int,
    current_user: User = Depends(get_current_active_user),
    workspace_service: WorkspaceService = Depends(get_workspace_service),
    member_service: WorkspaceMemberService = Depends(get_workspace_member_service),
) -> Workspace:
    workspace = await workspace_service.get_workspace(workspace_id)

    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    member = await member_service.repository.get_member(
        workspace_id=workspace_id,
        user_id=current_user.id,
    )

    if member is None or member.role != WorkspaceMemberRole.OWNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Workspace owner permission required",
        )

    return workspace