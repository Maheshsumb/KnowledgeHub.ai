import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_members_by_owner(client: AsyncClient, organization, owner_token):
    response = await client.get(
        f"/organizations/{organization.id}/members",
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) >= 4 

@pytest.mark.asyncio
async def test_list_members_by_viewer(client: AsyncClient, organization, viewer_token):
    response = await client.get(
        f"/organizations/{organization.id}/members",
        headers={"Authorization": f"Bearer {viewer_token}"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_list_members_not_member(client: AsyncClient, organization, test_token):
    response = await client.get(
        f"/organizations/{organization.id}/members",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code in [403, 404]
