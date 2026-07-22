import pytest
from httpx import AsyncClient

@pytest.mark.xfail(reason="Endpoint not implemented")
@pytest.mark.asyncio
async def test_owner_permissions(client: AsyncClient, organization, owner_token):
    # Owner can delete org
    response = await client.delete(
        f"/organizations/{organization.id}",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_admin_permissions(client: AsyncClient, organization, admin_token, owner_user):
    user, _ = owner_user
    # Admin cannot remove owner
    response = await client.delete(
        f"/organizations/{organization.id}/members/{user.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_member_permissions(client: AsyncClient, organization, member_token, test_user):
    user, _ = test_user
    # Member cannot add member
    response = await client.post(
        f"/organizations/{organization.id}/members",
        json={"user_id": str(user.id), "role": "viewer"},
        headers={"Authorization": f"Bearer {member_token}"}
    )
    assert response.status_code == 403
    
    # Member cannot remove member
    response = await client.delete(
        f"/organizations/{organization.id}/members/{user.id}",
        headers={"Authorization": f"Bearer {member_token}"}
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_viewer_permissions(client: AsyncClient, organization, viewer_token, test_user):
    user, _ = test_user
    # Viewer cannot add member
    response = await client.post(
        f"/organizations/{organization.id}/members",
        json={"user_id": str(user.id), "role": "viewer"},
        headers={"Authorization": f"Bearer {viewer_token}"}
    )
    assert response.status_code == 403
