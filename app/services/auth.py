from app.auth.hashing import hash_password, verify_password
from app.auth.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.repositories.refresh_token import RefreshTokenRepository
from app.repositories.user import UserRepository


class AuthService:

    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository

    async def register(
        self,
        data: dict,
    ):
        existing_user = await self.user_repository.get_by_email(
            data["email"]
        )

        if existing_user is not None:
            return None

        data["hashed_password"] = hash_password(
            data.pop("password")
        )

        return await self.user_repository.create(data)

    async def login(
        self,
        email: str,
        password: str,
    ):
        user = await self.user_repository.get_by_email(email)

        if user is None:
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None

        access_token = create_access_token(
            str(user.id)
        )

        refresh_token = create_refresh_token(
            str(user.id)
        )

        await self.refresh_token_repository.create(
            {
                "user_id": user.id,
                "token": refresh_token,
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh(
        self,
        refresh_token: str,
    ):
        stored_token = await self.refresh_token_repository.get_active_token(
            refresh_token
        )

        if stored_token is None:
            return None

        payload = decode_token(refresh_token)

        if payload is None:
            return None

        if payload.get("type") != "refresh":
            return None

        user_id = payload.get("sub")

        if user_id is None:
            return None

        user = await self.user_repository.get_by_id(
            int(user_id)
        )

        if user is None:
            return None

        new_access_token = create_access_token(
            str(user.id)
        )

        new_refresh_token = create_refresh_token(
            str(user.id)
        )

        await self.refresh_token_repository.update(
            stored_token,
            {
                "is_revoked": True,
            }
        )

        await self.refresh_token_repository.create(
            {
                "user_id": user.id,
                "token": new_refresh_token,
            }
        )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }

    async def logout(
        self,
        refresh_token: str,
    ) -> bool:
        stored_token = await self.refresh_token_repository.get_active_token(
            refresh_token
        )

        if stored_token is None:
            return False

        await self.refresh_token_repository.update(
            stored_token,
            {
                "is_revoked": True,
            }
        )

        return True