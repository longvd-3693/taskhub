from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_user_service
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse
)
from app.services.user import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "",
    response_model=UserResponse
)
def create_user(
    request: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return service.create_user(
        request.model_dump()
    )


@router.get(
    "",
    response_model=list[UserResponse]
)
def get_users(
    service: UserService = Depends(get_user_service)
):
    return service.get_users()


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    user = service.get_user(user_id)

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
def update_user(
    user_id: int,
    request: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    user = service.update_user(
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
    "/{user_id}"
)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    deleted = service.delete_user(user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "success": True
    }