import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_logout_successfully(client: AsyncClient, test_user):
    user, password = test_user
    login_res = await client.post(
        "/auth/login",
        json={"email": user.email, "password": password}
    )
    refresh_token = login_res.json()["refresh_token"]
    access_token = login_res.json()["access_token"]
    
    response = await client.post(
        "/auth/logout",
        json={"refresh_token": refresh_token},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    
    # Verify cannot refresh after logout
    refresh_res = await client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert refresh_res.status_code == 401
