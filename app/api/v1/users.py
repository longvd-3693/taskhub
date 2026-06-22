from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user, require_admin
from app.dependencies import get_user_service
from app.exceptions.exceptions import UserNotFound
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.services.user import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create User",
    description="Create a new user account.",
    responses={
        201: {"description": "User successfully created"},
        409: {"description": "User already exists"},
        422: {"description": "Validation error"},
    },
)
async def create_user(
    request: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return await service.create_user(
        request.model_dump()
    )


@router.get(
    "",
    response_model=list[UserResponse],
    summary="List Users",
    description="Retrieve a paginated list of all users.",
)
async def get_users(
    page: int = 1,
    limit: int = 20,
    service: UserService = Depends(get_user_service)
):
    return await service.get_users(
        page=page,
        limit=limit
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get Current User",
    description="Retrieve the authenticated user's profile information.",
    responses={
        200: {"description": "Current user information"},
        401: {"description": "Unauthorized"},
    },
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get User",
    description="Retrieve a user by ID.",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"},
    },
)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    user = await service.get_user(user_id)

    if user is None:
        raise UserNotFound()

    return user


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update User",
    description="Update user information by ID.",
    responses={
        200: {"description": "User updated successfully"},
        404: {"description": "User not found"},
        422: {"description": "Validation error"},
    },
)
async def update_user(
    user_id: int,
    request: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    user = await service.update_user(
        user_id,
        request.model_dump(
            exclude_none=True
        )
    )

    if user is None:
        raise UserNotFound()

    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete User",
    description="Delete a user by ID (admin only).",
    responses={
        204: {"description": "User deleted successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Insufficient permissions (admin required)"},
        404: {"description": "User not found"},
    },
)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(require_admin),
):
    success = await service.delete_user(user_id)

    if not success:
        raise UserNotFound()

    return None