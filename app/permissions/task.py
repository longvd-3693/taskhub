from fastapi import Depends

from app.auth.dependencies import get_current_active_user
from app.dependencies import get_task_service
from app.models.enums import WorkspaceMemberRole
from app.models.task import Task
from app.models.user import User
from app.services.task import TaskService
from app.exceptions.exceptions import (
    TaskNotFound,
    TaskPermissionDenied,
)


async def require_task_editor(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service),
) -> Task:
    task = await task_service.get_task_with_project_workspace(task_id)

    if task is None:
        raise TaskNotFound()

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
        raise TaskPermissionDenied(
            "Task editor permission required",
        )

    return task
