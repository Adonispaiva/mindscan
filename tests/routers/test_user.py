import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_user_profile(async_client: AsyncClient, auth_header):
    response = await async_client.get("/user/profile", headers=auth_header)
    assert response.status_code == 200
    assert "username" in response.json()


@pytest.mark.asyncio
async def test_update_user_profile(async_client: AsyncClient, auth_header):
    update = {"bio": "Atualizado via teste."}
    response = await async_client.put("/user/profile", json=update, headers=auth_header)
    assert response.status_code == 200
    assert response.json().get("bio") == "Atualizado via teste."


@pytest.mark.asyncio
async def test_user_profile_requires_auth(async_client: AsyncClient):
    response = await async_client.get("/user/profile")
    assert response.status_code == 401
