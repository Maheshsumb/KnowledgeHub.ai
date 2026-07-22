import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests.factories.organization_factory import create_organization
from tests.factories.membership_factory import create_membership
from app.models.enums import OrganizationRole

@pytest.mark.xfail(reason="Endpoint not implemented")
@pytest.mark.asyncio
async def test_update_organization_success(client: AsyncClient, test_token, test_user, db_session: AsyncSession):
    user, _ = test_user
    org = await create_organization(db_session, owner_id=user.id)
    await create_membership(db_session, user.id, org.id, OrganizationRole.OWNER)
    
    response = await client.patch(
        f"/organizations/{org.id}",
        json={"name": "Updated Org"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Org"

@pytest.mark.xfail(reason="Endpoint not implemented")
@pytest.mark.asyncio
async def test_update_organization_unauthorized(client: AsyncClient, db_session: AsyncSession, test_user):
    user, _ = test_user
    org = await create_organization(db_session, owner_id=user.id)
    
    response = await client.patch(
        f"/organizations/{org.id}",
        json={"name": "Updated Org"},
        headers={"Authorization": "Bearer invalid"}
    )
    assert response.status_code == 401
