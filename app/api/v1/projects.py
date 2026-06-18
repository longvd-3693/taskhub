from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_project_service
from app.models.project import Project
from app.permissions.project import require_project_editor
from app.permissions.workspace_member import require_workspace_editor
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.project import ProjectService
from app.permissions.project import (
    require_project_member,
)

router = APIRouter(
    tags=["Projects"],
)


@router.post(
    "/workspaces/{workspace_id}/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    request: ProjectCreate,
    workspace_id: int,
    current_user=Depends(require_workspace_editor),
    service: ProjectService = Depends(get_project_service),
):
    return await service.create_project(
        workspace_id=workspace_id,
        data=request.model_dump(),
    )


@router.get(
    "/projects/{project_id}",
    response_model=ProjectResponse,
)
async def get_project(
    project_id: int,
    service: ProjectService = Depends(require_project_member),
):
    project = await service.get_project(project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


@router.patch(
    "/projects/{project_id}",
    response_model=ProjectResponse,
)
async def update_project(
    request: ProjectUpdate,
    project: Project = Depends(require_project_editor),
    service: ProjectService = Depends(get_project_service),
):
    return await service.update_project(
        project,
        request.model_dump(exclude_none=True),
    )


@router.patch(
    "/projects/{project_id}/archive",
    response_model=ProjectResponse,
)
async def archive_project(
    project: Project = Depends(require_project_editor),
    service: ProjectService = Depends(get_project_service),
):
    return await service.archive_project(project)


@router.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project: Project = Depends(require_project_editor),
    service: ProjectService = Depends(get_project_service),
):
    await service.delete_project(project)

    return None