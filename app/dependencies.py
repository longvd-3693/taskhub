from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.repositories.workspace import WorkspaceRepository
from app.services.workspace import WorkspaceService
from app.repositories.project import ProjectRepository
from app.repositories.task import TaskRepository
from app.services.project import ProjectService
from app.services.task import TaskService
from app.repositories.refresh_token import RefreshTokenRepository
from app.services.auth import AuthService
from app.repositories.workspace_member import WorkspaceMemberRepository
from app.services.workspace_member import WorkspaceMemberService



def get_user_repository(
    db: AsyncSession = Depends(get_db)
):
    return UserRepository(db)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository)
):
    return UserService(repository)


def get_workspace_repository(
    db: AsyncSession = Depends(get_db),
):
    return WorkspaceRepository(db)



def get_project_repository(
    db: AsyncSession = Depends(get_db),
):
    return ProjectRepository(db)


def get_project_service(
    repository: ProjectRepository = Depends(get_project_repository),
):
    return ProjectService(repository)


def get_task_repository(
    db: AsyncSession = Depends(get_db),
):
    return TaskRepository(db)


def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
):
    return TaskService(repository)

def get_refresh_token_repository(
    db: AsyncSession = Depends(get_db),
):
    return RefreshTokenRepository(db)

def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    refresh_token_repository: RefreshTokenRepository = Depends(
        get_refresh_token_repository
    ),
):
    return AuthService(
        user_repository=user_repository,
        refresh_token_repository=refresh_token_repository,
    )


def get_workspace_member_repository(
    db: AsyncSession = Depends(get_db),
):
    return WorkspaceMemberRepository(db)


def get_workspace_service(
    repository: WorkspaceRepository = Depends(get_workspace_repository),
    member_repository: WorkspaceMemberRepository = Depends(
        get_workspace_member_repository
    ),
):
    return WorkspaceService(
        repository=repository,
        member_repository=member_repository,
    )

def get_workspace_member_service(
    repository: WorkspaceMemberRepository = Depends(
        get_workspace_member_repository
    ),
):
    return WorkspaceMemberService(repository)
