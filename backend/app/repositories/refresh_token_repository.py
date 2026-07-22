from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        user_id,
        token_id,
        expires_at,
    ):
        token = RefreshToken(
            user_id=user_id,
            token_id=token_id,
            expires_at=expires_at,
        )

        self.db.add(token)
        await self.db.commit()
        await self.db.refresh(token)

        return token

    async def get_by_jti(self, jti):
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.token_id == jti
            )
        )

        return result.scalar_one_or_none()

    async def revoke(self, token, replaced_by=None):
        token.revoked = True
        token.replaced_by = replaced_by

        await self.db.commit()

    async def revoke_all_for_user(self, user_id):
        await self.db.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id)
            .values(revoked=True)
        )
        await self.db.commit()

async def revoke_by_jti(self, jti: str):
    token = await self.get_by_jti(jti)

    if token is None:
        return False

    token.revoked = True

    await self.db.commit()

    return True
