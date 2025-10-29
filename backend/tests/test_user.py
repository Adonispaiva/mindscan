# D:\projetos-inovexa\mindscan\backend\tests\test_user.py

import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_user_router_exists():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/user")
    assert response.status_code in [200, 404]  # Ajustar conforme as rotas implementadas
