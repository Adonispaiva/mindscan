import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_list_users_as_admin(async_client: AsyncClient, admin_header):
    response = await async_client.get("/admin/users", headers=admin_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_admin_requires_auth(async_client: AsyncClient):
    response = await async_client.get("/admin/users")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_non_admin_access_denied(async_client: AsyncClient, auth_header):
    response = await async_client.get("/admin/users", headers=auth_header)
    assert response.status_code == 403
