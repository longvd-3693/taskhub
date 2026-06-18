from fastapi import APIRouter, Depends, Query, status

from app.auth.dependencies import get_current_active_user
from app.dependencies import get_task_service
from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from app.permissions.project import (
    require_project_editor,
    require_project_member,
)
from app.permissions.task import require_task_editor
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task import TaskService


router = APIRouter(
    tags=["Tasks"],
)


@router.get(
    "/projects/{project_id}/tasks",
    response_model=list[TaskResponse],
)
async def get_project_tasks(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    project: Project = Depends(require_project_member),
    service: TaskService = Depends(get_task_service),
):
    return await service.get_project_tasks(
        project_id=project.id,
        page=page,
        limit=limit,
    )


@router.post(
    "/projects/{project_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    request: TaskCreate,
    project: Project = Depends(require_project_editor),
    current_user: User = Depends(get_current_active_user),
    service: TaskService = Depends(get_task_service),
):
    return await service.create_task(
        project_id=project.id,
        created_by=current_user.id,
        data=request.model_dump(),
    )


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
)
async def update_task(
    request: TaskUpdate,
    task: Task = Depends(require_task_editor),
    service: TaskService = Depends(get_task_service),
):
    return await service.update_task(
        task,
        request.model_dump(exclude_none=True),
    )


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task: Task = Depends(require_task_editor),
    service: TaskService = Depends(get_task_service),
):
    await service.delete_task(task)

    return None