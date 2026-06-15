from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_task_service
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task import TaskService


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreate,
    service: TaskService = Depends(get_task_service),
):
    return await service.create_task(request.model_dump())


@router.get("", response_model=list[TaskResponse])
async def get_tasks(
    page: int = 1,
    limit: int = 20,
    service: TaskService = Depends(get_task_service),
):
    return await service.get_tasks(page=page, limit=limit)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    task = await service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    request: TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    task = await service.update_task(
        task_id,
        request.model_dump(exclude_none=True),
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    success = await service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None