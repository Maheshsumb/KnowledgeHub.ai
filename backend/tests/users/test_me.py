import pytest
from httpx import AsyncClient
from jose import jwt
from datetime import datetime, timedelta, UTC
from app.core.config import settings

@pytest.mark.asyncio
async def test_get_me_valid_jwt(client: AsyncClient, test_token, test_user):
    user, _ = test_user
    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == user.email

@pytest.mark.asyncio
async def test_get_me_invalid_jwt(client: AsyncClient):
    response = await client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_me_expired_jwt(client: AsyncClient):
    expire = datetime.now(UTC) - timedelta(minutes=1)
    payload = {"sub": "fake_id", "exp": expire, "type": "access"}
    expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_me_no_authorization_header(client: AsyncClient):
    response = await client.get("/users/me")
    assert response.status_code == 401
