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
# ✅ TESTE: CRIAÇÃO DE QUIZ
# ----------------------
@pytest.mark.asyncio
async def test_create_quiz(client):
    payload = {
        "title": "MindScan Quiz",
        "description": "Avaliação cognitiva inicial"
    }
    response = await client.post("/quiz/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data

# ----------------------
# ✅ TESTE: LISTAGEM DE QUIZZES
# ----------------------
@pytest.mark.asyncio
async def test_list_quizzes(client):
    response = await client.get("/quiz/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ----------------------
# ✅ TESTE: GET QUIZ POR ID
# ----------------------
@pytest.mark.asyncio
async def test_get_quiz_by_id(client):
    payload = {
        "title": "Quiz ID Test",
        "description": "Teste de busca por ID"
    }
    create_resp = await client.post("/quiz/", json=payload)
    quiz_id = create_resp.json()["id"]

    response = await client.get(f"/quiz/{quiz_id}")
    assert response.status_code == 200
    assert response.json()["id"] == quiz_id

# ----------------------
# ✅ TESTE: UPDATE DE QUIZ
# ----------------------
@pytest.mark.asyncio
async def test_update_quiz(client):
    payload = {
        "title": "Quiz Original",
        "description": "Descrição original"
    }
    create_resp = await client.post("/quiz/", json=payload)
    quiz_id = create_resp.json()["id"]

    update_data = {
        "title": "Quiz Atualizado"
    }
    response = await client.put(f"/quiz/{quiz_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]

# ----------------------
# ✅ TESTE: DELETE DE QUIZ
# ----------------------
@pytest.mark.asyncio
async def test_delete_quiz(client):
    payload = {
        "title": "Quiz para Deletar",
        "description": "Será excluído"
    }
    create_resp = await client.post("/quiz/", json=payload)
    quiz_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/quiz/{quiz_id}")
    assert delete_resp.status_code == 204

    get_resp = await client.get(f"/quiz/{quiz_id}")
    assert get_resp.status_code == 404
