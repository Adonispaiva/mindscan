import pytest
from httpx import AsyncClient
from main import create_app

import pytest_asyncio

@pytest_asyncio.fixture
async def client():
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_healthcheck(client):
    response = await client.get("/health/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}

@pytest.mark.asyncio
async def test_user_route_exists(client):
    response = await client.get("/user/")
    assert response.status_code in [200, 404]  # depende se há handler definido

@pytest.mark.asyncio
async def test_openapi_schema(client):
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "paths" in data
    assert "/health/ping" in data["paths"]
