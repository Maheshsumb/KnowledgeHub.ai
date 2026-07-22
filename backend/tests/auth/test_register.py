import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.users import User

@pytest.mark.asyncio
async def test_register_success(client: AsyncClient, db_session: AsyncSession):
    response = await client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!",
            "full_name": "New User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    
    # Verify in DB
    result = await db_session.execute(select(User).where(User.email == "newuser@example.com"))
    user = result.scalars().first()
    assert user is not None

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, test_user):
    user, _ = test_user
    response = await client.post(
        "/auth/register",
        json={
            "email": user.email,
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!",
            "full_name": "Duplicate User"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_register_weak_password(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={
            "email": "weak@example.com",
            "password": "weak",
            "confirm_password": "weak",
            "full_name": "Weak User"
        }
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_register_invalid_email(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={
            "email": "not-an-email",
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!",
            "full_name": "Invalid Email"
        }
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_register_missing_fields(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={"email": "missing@example.com"}
    )
    assert response.status_code == 422
