from datetime import datetime, UTC
from app.schemas.token import TokenResponse
from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    PasswordMismatchError,
)
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    decode_token,
)
from app.models.users import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repo: UserRepository,refresh_repo: RefreshTokenRepository):
        self.repo = repo
        self.refresh_repo = refresh_repo

    async def register(self, full_name, email, password,com_pass):
        existing = await self.repo.get_by_email(email)

        if existing:
            raise EmailAlreadyExistsError("Email already exists")
        if password!=com_pass:
            raise PasswordMismatchError("Passwords do not match")

        user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
        )

        return await self.repo.create(user)

    async def login(self, email, password):
        user = await self.repo.get_by_email(email)

        if not user:
            raise InvalidCredentialsError("Invalid email or password")

        if not user.is_active:
            raise InvalidCredentialsError("User account is inactive")

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid email or password")
        access_token = create_access_token(str(user.id))

        refresh_token, jti, expires_at = create_refresh_token(
            str(user.id)
        )

        await self.refresh_repo.create(
            user_id=user.id,
            token_id=jti,
            expires_at=expires_at,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
    async def refresh(self, refresh_token: str):
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise InvalidRefreshTokenError("Invalid refresh token")

        jti = payload["jti"]
        stored_token = await self.refresh_repo.get_by_jti(jti)

        if stored_token is None:
            raise InvalidRefreshTokenError("Refresh token not found")

        if stored_token.expires_at < datetime.now(UTC):
            raise InvalidRefreshTokenError("Refresh token expired")

        if stored_token.revoked:
            await self.refresh_repo.revoke_all_for_user(stored_token.user_id)
            raise InvalidRefreshTokenError("Refresh token has been revoked")

        user = await self.repo.get_by_id(payload["sub"])

        if user is None:
            raise InvalidCredentialsError("User not found")

        if not user.is_active:
            raise InvalidCredentialsError("User account is inactive")

        access_token = create_access_token(str(user.id))

        new_refresh_token, new_jti, expires_at = create_refresh_token(
            str(user.id)
        )

        await self.refresh_repo.revoke(stored_token, replaced_by=new_jti)

        await self.refresh_repo.create(
            user_id=user.id,
            token_id=new_jti,
            expires_at=expires_at,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )

    async def logout(self, refresh_token: str):

        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise InvalidRefreshTokenError(
                "Invalid refresh token"
            )

        jti = payload["jti"]

        token = await self.refresh_repo.get_by_jti(jti)

        if token is None:
            raise InvalidRefreshTokenError(
                "Refresh token not found"
            )

        if token.revoked:
            raise InvalidRefreshTokenError(
                "Refresh token already revoked"
            )

        await self.refresh_repo.revoke(token)

        return {
            "message": "Logged out successfully"
        }