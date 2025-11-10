import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    response = await async_client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "strongpassword"
    })
    assert response.status_code == 201
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_user(async_client: AsyncClient):
    # Pré-condição: usuário já registrado
    await async_client.post("/auth/register", json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "strongpassword"
    })

    response = await async_client.post("/auth/login", data={
        "username": "loginuser",
        "password": "strongpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_fail(async_client: AsyncClient):
    response = await async_client.post("/auth/login", data={
        "username": "wronguser",
        "password": "wrongpass"
    })
    assert response.status_code == 401
