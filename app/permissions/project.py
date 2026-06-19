from fastapi import Depends

from app.auth.dependencies import get_current_active_user
from app.dependencies import get_project_service
from app.models.enums import WorkspaceMemberRole
from app.models.project import Project
from app.models.user import User
from app.services.project import ProjectService
from app.exceptions.exceptions import (
    ProjectNotFound,
    ProjectPermissionDenied,
)


async def _get_project_member(
    project_id: int,
    current_user: User,
    project_service: ProjectService,
):
    project = await project_service.get_project_with_workspace(project_id)

    if project is None:
        raise ProjectNotFound()

    member = next(
        (
            member
            for member in project.workspace.members
            if member.user_id == current_user.id
        ),
        None,
    )

    if member is None:
        raise ProjectPermissionDenied("Workspace member permission required")

    return project, member.role


async def require_project_member(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    project_service: ProjectService = Depends(get_project_service),
) -> Project:
    project, _ = await _get_project_member(
        project_id,
        current_user,
        project_service,
    )

    return project


async def require_project_editor(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    project_service: ProjectService = Depends(get_project_service),
) -> Project:
    project, role = await _get_project_member(
        project_id,
        current_user,
        project_service,
    )

    if role not in (
        WorkspaceMemberRole.OWNER,
        WorkspaceMemberRole.EDITOR,
    ):
        raise ProjectPermissionDenied("Project editor permission required")

    return project
