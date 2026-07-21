from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.users import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, full_name, email, password,com_pass):
        existing = await self.repo.get_by_email(email)

        if existing:
            raise ValueError("Email already exists")
        if password!=com_pass:
            raise ValueError("Passwords do not match")

        user = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
        )

        return await self.repo.create(user)

    async def login(self, email, password):
        user = await self.repo.get_by_email(email)

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return {
            "access_token": create_access_token(str(user.id)),
            "refresh_token": create_refresh_token(str(user.id)),
        }