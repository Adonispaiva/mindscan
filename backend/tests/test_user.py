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
# ✅ TESTE: CRIAÇÃO
# ----------------------
@pytest.mark.asyncio
async def test_create_user(client):
    payload = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "securepassword"
    }
    response = await client.post("/user/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == payload["username"]
    assert "id" in data

# ----------------------
# ✅ TESTE: LISTAGEM
# ----------------------
@pytest.mark.asyncio
async def test_user_list(client):
    response = await client.get("/user/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ----------------------
# ✅ TESTE: BUSCA POR ID
# ----------------------
@pytest.mark.asyncio
async def test_get_user_by_id(client):
    # Cria um novo usuário
    payload = {
        "username": "user_get",
        "email": "get@example.com",
        "password": "getpass"
    }
    create_resp = await client.post("/user/", json=payload)
    user_id = create_resp.json()["id"]

    # Busca o usuário pelo ID
    response = await client.get(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id

# ----------------------
# ✅ TESTE: UPDATE
# ----------------------
@pytest.mark.asyncio
async def test_update_user(client):
    payload = {
        "username": "user_update",
        "email": "update@example.com",
        "password": "updatepass"
    }
    create_resp = await client.post("/user/", json=payload)
    user_id = create_resp.json()["id"]

    update_data = {
        "username": "user_updated"
    }
    response = await client.put(f"/user/{user_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["username"] == update_data["username"]

# ----------------------
# ✅ TESTE: DELETE
# ----------------------
@pytest.mark.asyncio
async def test_delete_user(client):
    payload = {
        "username": "user_delete",
        "email": "delete@example.com",
        "password": "deletepass"
    }
    create_resp = await client.post("/user/", json=payload)
    user_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/user/{user_id}")
    assert delete_resp.status_code == 204

    # Verifica se realmente foi removido
    get_resp = await client.get(f"/user/{user_id}")
    assert get_resp.status_code == 404
