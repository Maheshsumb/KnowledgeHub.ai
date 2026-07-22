import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.organization import Organization
from app.models.membership import Membership
from app.models.enums import OrganizationRole

@pytest.mark.asyncio
async def test_create_organization_success(client: AsyncClient, test_token, db_session: AsyncSession):
    response = await client.post(
        "/organizations",
        json={"name": "New Org", "description": "A new org"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Org"
    assert "slug" in data
    
    org_id = data["id"]
    
    # Verify owner membership automatically created
    result = await db_session.execute(select(Membership).where(Membership.organization_id == org_id))
    memberships = result.scalars().all()
    assert len(memberships) == 1
    assert memberships[0].role == OrganizationRole.OWNER

@pytest.mark.asyncio
async def test_create_organization_invalid_name(client: AsyncClient, test_token):
    # A validation error should be thrown for missing required fields
    response = await client.post(
        "/organizations",
        json={}, 
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_organization_missing_jwt(client: AsyncClient):
    response = await client.post(
        "/organizations",
        json={"name": "New Org"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_organization_invalid_jwt(client: AsyncClient):
    response = await client.post(
        "/organizations",
        json={"name": "New Org"},
        headers={"Authorization": "Bearer invalid"}
    )
    assert response.status_code == 401
