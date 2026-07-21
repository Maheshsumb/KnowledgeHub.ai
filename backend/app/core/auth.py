from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.databases.session import get_db
from app.repositories.user_repository import UserRepository
from fastapi.security import HTTPAuthorizationCredentials
from app.core.security import bearer_scheme

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: AsyncSession = Depends(get_db),
):
    token = credentials.credentials
    payload = decode_token(token)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type",
        )

    user_id = payload.get("sub")

    repo = UserRepository(db)

    user = await repo.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User is inactive",
        )

    return user