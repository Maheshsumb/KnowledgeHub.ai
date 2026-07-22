import pytest
from httpx import AsyncClient

@pytest.mark.xfail(reason="Endpoint not fully implemented")
@pytest.mark.asyncio
async def test_remove_member_owner_removes_member(client: AsyncClient, organization, owner_token, member_user):
    user, _ = member_user
    response = await client.delete(
        f"/organizations/{organization.id}/members/{user.id}",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert response.status_code == 204

@pytest.mark.xfail(reason="Endpoint not fully implemented")
@pytest.mark.asyncio
async def test_remove_member_admin_removes_viewer(client: AsyncClient, organization, admin_token, viewer_user):
    user, _ = viewer_user
    response = await client.delete(
        f"/organizations/{organization.id}/members/{user.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_remove_member_admin_removes_owner(client: AsyncClient, organization, admin_token, owner_user):
    user, _ = owner_user
    response = await client.delete(
        f"/organizations/{organization.id}/members/{user.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_remove_member_yourself(client: AsyncClient, organization, member_token, member_user):
    user, _ = member_user
    response = await client.delete(
        f"/organizations/{organization.id}/members/{user.id}",
        headers={"Authorization": f"Bearer {member_token}"}
    )
    assert response.status_code == 403
