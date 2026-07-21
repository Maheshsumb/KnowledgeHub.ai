from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.databases.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.token import TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(UserRepository(db))

    try:
        user = await service.register(
            request.full_name,
            request.email,
            request.password,
            request.confirm_password,
        )
        return {
            "id": str(user.id),
            "email": user.email,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(UserRepository(db))

    tokens = await service.login(
        request.email,
        request.password,
    )

    if not tokens:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return tokens