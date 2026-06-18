from fastapi import Depends, HTTPException, status

from app.auth.dependencies import get_current_active_user
from app.dependencies import get_task_service
from app.models.enums import WorkspaceMemberRole
from app.models.task import Task
from app.models.user import User
from app.services.task import TaskService


async def require_task_editor(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service),
) -> Task:
    task = await task_service.get_task_with_project_workspace(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    member = next(
        (
            member
            for member in task.project.workspace.members
            if member.user_id == current_user.id
        ),
        None,
    )

    if member is None or member.role not in [
        WorkspaceMemberRole.OWNER,
        WorkspaceMemberRole.EDITOR,
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Task editor permission required",
        )

    return task