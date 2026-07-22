import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user):
    user, password = test_user
    response = await client.post(
        "/auth/login",
        json={
            "email": user.email,
            "password": password
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user):
    user, _ = test_user
    response = await client.post(
        "/auth/login",
        json={
            "email": user.email,
            "password": "WrongPassword!"
        }
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_unknown_email(client: AsyncClient):
    response = await client.post(
        "/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "Password123!"
        }
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_missing_fields(client: AsyncClient):
    response = await client.post(
        "/auth/login",
        json={"email": "missing@example.com"}
    )
    assert response.status_code == 422
