from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import (
    get_workspace_member_service,
    get_workspace_service,
)
from app.models.workspace import Workspace
from app.permissions.workspace import require_workspace_owner
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceResponse,
)
from app.schemas.workspace_member import (
    WorkspaceMemberCreate,
    WorkspaceMemberResponse,
)
from app.services.workspace import WorkspaceService
from app.services.workspace_member import WorkspaceMemberService

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"],
)


@router.post(
    "",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_workspace(
    request: WorkspaceCreate,
    service: WorkspaceService = Depends(get_workspace_service),
):
    return await service.create_workspace(request.model_dump())


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
async def get_workspace(
    workspace_id: int,
    service: WorkspaceService = Depends(get_workspace_service),
):
    workspace = await service.get_workspace(workspace_id)

    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    return workspace


@router.post(
    "/{workspace_id}/members",
    response_model=WorkspaceMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_workspace_member(
    request: WorkspaceMemberCreate,
    workspace: Workspace = Depends(require_workspace_owner),
    service: WorkspaceMemberService = Depends(get_workspace_member_service),
):
    member = await service.add_member(
        workspace_id=workspace.id,
        user_id=request.user_id,
        role=request.role,
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a workspace member",
        )

    return member


@router.delete(
    "/{workspace_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_workspace_member(
    user_id: int,
    workspace: Workspace = Depends(require_workspace_owner),
    service: WorkspaceMemberService = Depends(get_workspace_member_service),
):
    success = await service.remove_member(
        workspace_id=workspace.id,
        user_id=user_id,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace member not found or cannot remove owner",
        )

    return None