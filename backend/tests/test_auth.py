import pytest
import pytest_asyncio
from httpx import AsyncClient
from main import create_app

# ------------------
# 🔧 FIXTURE GLOBAL
# ------------------
@pytest_asyncio.fixture
async def client():
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# ----------------------
# ✅ TESTE: LOGIN VÁLIDO
# ----------------------
@pytest.mark.asyncio
async def test_valid_login(client):
    payload = {
        "username": "auth_user",
        "email": "auth@example.com",
        "password": "authpass"
    }
    # Cria o usuário
    await client.post("/user/", json=payload)

    login_data = {
        "username": payload["username"],
        "password": payload["password"]
    }
    response = await client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

# ----------------------
# ✅ TESTE: LOGIN INVÁLIDO
# ----------------------
@pytest.mark.asyncio
async def test_invalid_login(client):
    login_data = {
        "username": "nonexistent",
        "password": "wrongpass"
    }
    response = await client.post("/auth/login", json=login_data)
    assert response.status_code == 401

# ----------------------
# ✅ TESTE: TOKEN JWT
# ----------------------
@pytest.mark.asyncio
async def test_access_protected_route(client):
    payload = {
        "username": "secure_user",
        "email": "secure@example.com",
        "password": "securepass"
    }
    await client.post("/user/", json=payload)

    login_resp = await client.post("/auth/login", json={
        "username": payload["username"],
        "password": payload["password"]
    })
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/user/", headers=headers)
    assert response.status_code in [200, 403]  # Depende da permissão atribuída
