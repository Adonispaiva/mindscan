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
# ✅ TESTE: SUBMISSÃO DE RESPOSTA
# ----------------------
@pytest.mark.asyncio
async def test_submit_response(client):
    user_payload = {
        "username": "responder",
        "email": "responder@example.com",
        "password": "responderpass"
    }
    quiz_payload = {
        "title": "Quiz de Teste",
        "description": "Teste de submissão"
    }

    user_resp = await client.post("/user/", json=user_payload)
    quiz_resp = await client.post("/quiz/", json=quiz_payload)

    response_payload = {
        "user_id": user_resp.json()["id"],
        "quiz_id": quiz_resp.json()["id"],
        "answers": {"q1": "a", "q2": "b"}
    }
    response = await client.post("/response/", json=response_payload)
    assert response.status_code == 201
    assert response.json()["user_id"] == response_payload["user_id"]

# ----------------------
# ✅ TESTE: LISTAGEM DE RESPOSTAS
# ----------------------
@pytest.mark.asyncio
async def test_list_responses(client):
    response = await client.get("/response/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# ----------------------
# ✅ TESTE: GET POR ID
# ----------------------
@pytest.mark.asyncio
async def test_get_response_by_id(client):
    user = await client.post("/user/", json={
        "username": "getres",
        "email": "getres@example.com",
        "password": "123456"
    })
    quiz = await client.post("/quiz/", json={
        "title": "Quiz Resposta",
        "description": "Desc"
    })
    post_resp = await client.post("/response/", json={
        "user_id": user.json()["id"],
        "quiz_id": quiz.json()["id"],
        "answers": {"x": "y"}
    })
    response_id = post_resp.json()["id"]
    response = await client.get(f"/response/{response_id}")
    assert response.status_code == 200
    assert response.json()["id"] == response_id

# ----------------------
# ✅ TESTE: DELETE DE RESPOSTA
# ----------------------
@pytest.mark.asyncio
async def test_delete_response(client):
    user = await client.post("/user/", json={
        "username": "delres",
        "email": "delres@example.com",
        "password": "123456"
    })
    quiz = await client.post("/quiz/", json={
        "title": "Quiz Del",
        "description": "Del"
    })
    post_resp = await client.post("/response/", json={
        "user_id": user.json()["id"],
        "quiz_id": quiz.json()["id"],
        "answers": {"a": "b"}
    })
    response_id = post_resp.json()["id"]
    delete_resp = await client.delete(f"/response/{response_id}")
    assert delete_resp.status_code == 204
    get_resp = await client.get(f"/response/{response_id}")
    assert get_resp.status_code == 404