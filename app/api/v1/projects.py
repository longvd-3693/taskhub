from fastapi import APIRouter, Depends, status

from app.dependencies import get_project_service
from app.models.project import Project
from app.permissions.project import (
    require_project_editor,
    require_project_member,
)
from app.permissions.workspace_member import require_workspace_editor
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.project import ProjectService

router = APIRouter(
    tags=["Projects"],
)


@router.post(
    "/workspaces/{workspace_id}/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Project",
    description="Create a new project in a workspace (editor or higher).",
    responses={
        201: {"description": "Project successfully created"},
        401: {"description": "Unauthorized"},
        403: {"description": "Insufficient permissions (editor or higher required)"},
        404: {"description": "Workspace not found"},
        422: {"description": "Validation error"},
    },
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
    summary="Get Project",
    description="Retrieve a project by ID (member access required).",
    responses={
        200: {"description": "Project found"},
        401: {"description": "Unauthorized"},
        403: {"description": "Insufficient permissions (member access required)"},
        404: {"description": "Project not found"},
    },
)
async def get_project(
    project: Project = Depends(require_project_member),
):
    return project


@router.patch(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    summary="Update Project",
    description="Update a project (editor or higher).",
    responses={
        200: {"description": "Project updated successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Insufficient permissions (editor or higher required)"},
        404: {"description": "Project not found"},
        422: {"description": "Validation error"},
    },
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
    summary="Archive Project",
    description="Archive a project (editor or higher).",
    responses={
        200: {"description": "Project archived successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Insufficient permissions (editor or higher required)"},
        404: {"description": "Project not found"},
    },
)
async def archive_project(
    project: Project = Depends(require_project_editor),
    service: ProjectService = Depends(get_project_service),
):
    return await service.archive_project(project)


@router.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Project",
    description="Delete a project (editor or higher).",
    responses={
        204: {"description": "Project deleted successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Insufficient permissions (editor or higher required)"},
        404: {"description": "Project not found"},
    },
)
async def delete_project(
    project: Project = Depends(require_project_editor),
    service: ProjectService = Depends(get_project_service),
):
    await service.delete_project(project)

    return None