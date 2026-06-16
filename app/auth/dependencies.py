from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.auth.jwt import decode_token
from app.dependencies import get_user_service
from app.models.user import User
from app.services.user import UserService


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),
) -> User:
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    if payload.get("type") != "access":
         raise HTTPException(
             status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Invalid token",
         )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = await service.get_user(int(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user