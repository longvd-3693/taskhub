from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_auth_service
from app.exceptions.exceptions import (
    AuthenticationFailed,
    EmailAlreadyExists,
    InvalidRefreshToken,
    RefreshTokenNotFound,
)
from app.schemas.auth import (
    LogoutRequest,
    RefreshTokenRequest,
    TokenResponse,
)
from app.schemas.user import UserCreate, UserResponse
from app.services.auth import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: UserCreate,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.register(request.model_dump())

    if user is None:
        raise EmailAlreadyExists()

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    token = await service.login(
        email=form_data.username,
        password=form_data.password,
    )

    if token is None:
        raise AuthenticationFailed()

    return token


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
async def refresh(
    request: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service),
):
    token = await service.refresh(request.refresh_token)

    if token is None:
        raise InvalidRefreshToken()

    return token


@router.post("/logout")
async def logout(
    request: LogoutRequest,
    service: AuthService = Depends(get_auth_service),
):
    success = await service.logout(request.refresh_token)

    if not success:
        raise RefreshTokenNotFound()

    return {
        "message": "Logged out successfully",
    }
