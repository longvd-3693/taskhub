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
    summary="Register",
    description="Create a new user account with email and password.",
    responses={
        201: {"description": "User successfully created"},
        409: {"description": "Email already exists"},
        422: {"description": "Validation error"},
    },
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
    summary="Login",
    description="Authenticate a user and return access and refresh tokens.",
    responses={
        401: {
            "description": "Invalid email or password",
        },
        422: {
            "description": "Validation error",
        },
    },
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
    summary="Refresh Token",
    description="Refresh an expired access token using a valid refresh token.",
    responses={
        200: {"description": "Token refreshed successfully"},
        401: {"description": "Invalid or expired refresh token"},
        422: {"description": "Validation error"},
    },
)
async def refresh(
    request: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service),
):
    token = await service.refresh(request.refresh_token)

    if token is None:
        raise InvalidRefreshToken()

    return token


@router.post(
    "/logout",
    summary="Logout",
    description="Invalidate the current refresh token and log out the user.",
    responses={
        200: {"description": "Logged out successfully"},
        404: {"description": "Refresh token not found"},
        422: {"description": "Validation error"},
    },
)
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
