import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from main import app  # substitua por seu ponto de entrada se necessário


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def auth_header(async_client):
    user_data = {
        "username": "usuario_teste",
        "email": "teste@mindscan.com",
        "password": "12345678"
    }
    await async_client.post("/auth/register", json=user_data)
    login = await async_client.post("/auth/login", data={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def admin_header(async_client):
    admin_data = {
        "username": "admin_teste",
        "email": "admin@mindscan.com",
        "password": "admin123",
        "is_admin": True  # Presume-se que este campo seja tratado no backend
    }
    await async_client.post("/auth/register", json=admin_data)
    login = await async_client.post("/auth/login", data={
        "username": admin_data["username"],
        "password": admin_data["password"]
    })
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}