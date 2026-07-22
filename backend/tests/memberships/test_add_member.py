import pytest
from httpx import AsyncClient
from app.models.enums import OrganizationRole

@pytest.mark.xfail(reason="Endpoint not fully implemented")
@pytest.mark.asyncio
async def test_add_member_owner_adds_admin(client: AsyncClient, organization, owner_token, test_user):
    user, _ = test_user
    response = await client.post(
        f"/organizations/{organization.id}/members",
        json={"user_id": str(user.id), "role": OrganizationRole.ADMIN.value},
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert response.status_code == 201

@pytest.mark.xfail(reason="Endpoint not fully implemented")
@pytest.mark.asyncio
async def test_add_member_admin_adds_viewer(client: AsyncClient, organization, admin_token, test_user):
    user, _ = test_user
    response = await client.post(
        f"/organizations/{organization.id}/members",
        json={"user_id": str(user.id), "role": OrganizationRole.VIEWER.value},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201

@pytest.mark.xfail(reason="Endpoint not fully implemented")
@pytest.mark.asyncio
async def test_add_member_duplicate_member(client: AsyncClient, organization, owner_token, admin_user):
    user, _ = admin_user
    response = await client.post(
        f"/organizations/{organization.id}/members",
        json={"user_id": str(user.id), "role": OrganizationRole.MEMBER.value},
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert response.status_code in [400, 409] 
    
@pytest.mark.asyncio
async def test_add_member_invalid_role(client: AsyncClient, organization, owner_token, test_user):
    user, _ = test_user
    response = await client.post(
        f"/organizations/{organization.id}/members",
        json={"user_id": str(user.id), "role": "INVALID"},
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert response.status_code == 422
