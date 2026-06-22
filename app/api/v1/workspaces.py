from fastapi import APIRouter, Depends, status

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
from app.exceptions.exceptions import (
    ConflictException,
    WorkspaceNotFound,
)

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"],
)


@router.post(
    "",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Workspace",
    description="Create a new workspace.",
    responses={
        201: {"description": "Workspace successfully created"},
        422: {"description": "Validation error"},
    },
)
async def create_workspace(
    request: WorkspaceCreate,
    service: WorkspaceService = Depends(get_workspace_service),
):
    return await service.create_workspace(request.model_dump())


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
    summary="Get Workspace",
    description="Retrieve a workspace by ID.",
    responses={
        200: {"description": "Workspace found"},
        404: {"description": "Workspace not found"},
    },
)
async def get_workspace(
    workspace_id: int,
    service: WorkspaceService = Depends(get_workspace_service),
):
    workspace = await service.get_workspace(workspace_id)

    if workspace is None:
        raise WorkspaceNotFound()

    return workspace


@router.post(
    "/{workspace_id}/members",
    response_model=WorkspaceMemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Workspace Member",
    description="Add a new member to a workspace (owner only).",
    responses={
        201: {"description": "Member successfully added"},
        401: {"description": "Unauthorized"},
        403: {"description": "Insufficient permissions (owner required)"},
        404: {"description": "Workspace not found"},
        409: {"description": "User is already a workspace member"},
        422: {"description": "Validation error"},
    },
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
        raise ConflictException("User is already a workspace member")

    return member


@router.delete(
    "/{workspace_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove Workspace Member",
    description="Remove a member from a workspace (owner only).",
    responses={
        204: {"description": "Member successfully removed"},
        401: {"description": "Unauthorized"},
        403: {"description": "Insufficient permissions (owner required)"},
        404: {"description": "Workspace or member not found"},
    },
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
        raise WorkspaceNotFound("Workspace member not found or cannot remove owner")

    return None
