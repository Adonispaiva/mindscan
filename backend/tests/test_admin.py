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
# ✅ TESTE: CRIAÇÃO DE USUÁRIO ADMIN
# ----------------------
@pytest.mark.asyncio
async def test_create_admin_user(client):
    payload = {
        "username": "admin_user",
        "email": "admin@example.com",
        "password": "adminpass",
        "is_admin": True
    }
    response = await client.post("/admin/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["is_admin"] is True

# ----------------------
# ✅ TESTE: LISTAGEM DE ADMINS
# ----------------------
@pytest.mark.asyncio
async def test_list_admins(client):
    response = await client.get("/admin/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for admin in data:
        assert admin["is_admin"] is True

# ----------------------
# ✅ TESTE: DELETE ADMIN
# ----------------------
@pytest.mark.asyncio
async def test_delete_admin(client):
    payload = {
        "username": "admin_delete",
        "email": "delete_admin@example.com",
        "password": "deletepass",
        "is_admin": True
    }
    create_resp = await client.post("/admin/", json=payload)
    admin_id = create_resp.json()["id"]
    delete_resp = await client.delete(f"/admin/{admin_id}")
    assert delete_resp.status_code == 204
    get_resp = await client.get(f"/admin/{admin_id}")
    assert get_resp.status_code == 404