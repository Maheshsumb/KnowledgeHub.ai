import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from tests.factories.organization_factory import create_organization
from tests.factories.membership_factory import create_membership
from app.models.enums import OrganizationRole

@pytest.mark.xfail(reason="Endpoint not fully implemented")
@pytest.mark.asyncio
async def test_list_organizations_user_with_one_org(client: AsyncClient, test_token, test_user, db_session: AsyncSession):
    user, _ = test_user
    org = await create_organization(db_session, owner_id=user.id)
    await create_membership(db_session, user.id, org.id, OrganizationRole.OWNER)
    
    response = await client.get("/organizations", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert len(response.json()) == 1

@pytest.mark.xfail(reason="Endpoint not fully implemented")
@pytest.mark.asyncio
async def test_list_organizations_user_with_multiple_orgs(client: AsyncClient, test_token, test_user, db_session: AsyncSession):
    user, _ = test_user
    org1 = await create_organization(db_session, owner_id=user.id)
    org2 = await create_organization(db_session, owner_id=user.id)
    await create_membership(db_session, user.id, org1.id, OrganizationRole.OWNER)
    await create_membership(db_session, user.id, org2.id, OrganizationRole.OWNER)
    
    response = await client.get("/organizations", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.xfail(reason="Endpoint not fully implemented")
@pytest.mark.asyncio
async def test_list_organizations_user_with_zero_orgs(client: AsyncClient, test_token):
    response = await client.get("/organizations", headers={"Authorization": f"Bearer {test_token}"})
    assert response.status_code == 200
    assert len(response.json()) == 0

@pytest.mark.asyncio
async def test_list_organizations_unauthorized(client: AsyncClient):
    response = await client.get("/organizations")
    assert response.status_code == 401
