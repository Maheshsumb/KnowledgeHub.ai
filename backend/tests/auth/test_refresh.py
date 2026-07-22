import pytest
from httpx import AsyncClient
from jose import jwt
from datetime import datetime, timedelta, UTC
from app.core.config import settings

@pytest.mark.asyncio
async def test_refresh_valid_token(client: AsyncClient, test_user):
    user, password = test_user
    # First login to get a refresh token
    login_res = await client.post(
        "/auth/login",
        json={"email": user.email, "password": password}
    )
    refresh_token = login_res.json()["refresh_token"]
    
    # Now use refresh token
    response = await client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

@pytest.mark.asyncio
async def test_refresh_expired_token(client: AsyncClient, test_user):
    user, _ = test_user
    expire = datetime.now(UTC) - timedelta(days=1)
    payload = {"sub": str(user.id), "jti": "fake_jti", "type": "refresh", "exp": expire}
    expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    response = await client.post(
        "/auth/refresh",
        json={"refresh_token": expired_token}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_refresh_invalid_jwt(client: AsyncClient):
    response = await client.post(
        "/auth/refresh",
        json={"refresh_token": "invalid.jwt.token"}
    )
    assert response.status_code == 401
