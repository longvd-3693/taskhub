from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from app.dependencies import get_user_service
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse
)
from app.services.user import UserService
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.auth.dependencies import require_admin


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
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
    response_model=list[UserResponse]
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
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    user = await service.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.patch(
    "/{user_id}",
    response_model=UserResponse
)
async def update_user(
    user_id: int,
    request: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    user = await service.update_user(
        user_id,
        request.model_dump(
            exclude_none=True
        )
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(require_admin),
):
    success = await service.delete_user(user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return None
