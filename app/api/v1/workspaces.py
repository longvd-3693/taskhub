from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_workspace_service
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceUpdate,
    WorkspaceResponse,
)
from app.services.workspace import WorkspaceService


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
    "",
    response_model=list[WorkspaceResponse],
)
async def get_workspaces(
    page: int = 1,
    limit: int = 20,
    service: WorkspaceService = Depends(get_workspace_service),
):
    return await service.get_workspaces(page=page, limit=limit)


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


@router.patch(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
async def update_workspace(
    workspace_id: int,
    request: WorkspaceUpdate,
    service: WorkspaceService = Depends(get_workspace_service),
):
    workspace = await service.update_workspace(
        workspace_id,
        request.model_dump(exclude_none=True),
    )

    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    return workspace


@router.delete(
    "/{workspace_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_workspace(
    workspace_id: int,
    service: WorkspaceService = Depends(get_workspace_service),
):
    success = await service.delete_workspace(workspace_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    return None