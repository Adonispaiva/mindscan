import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_quiz(async_client: AsyncClient, auth_header):
    quiz_data = {
        "title": "Teste Cognitivo",
        "questions": [
            {"question": "Qual a cor do céu?", "options": ["Azul", "Verde"], "answer": "Azul"}
        ]
    }
    response = await async_client.post("/quiz/create", json=quiz_data, headers=auth_header)
    assert response.status_code == 201
    assert "quiz_id" in response.json()


@pytest.mark.asyncio
async def test_get_all_quizzes(async_client: AsyncClient, auth_header):
    response = await async_client.get("/quiz/all", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_quiz_by_id(async_client: AsyncClient, auth_header):
    # Cria quiz primeiro
    quiz_data = {
        "title": "Teste Simples",
        "questions": [
            {"question": "2+2?", "options": ["3", "4"], "answer": "4"}
        ]
    }
    creation = await async_client.post("/quiz/create", json=quiz_data, headers=auth_header)
    quiz_id = creation.json().get("quiz_id")

    response = await async_client.get(f"/quiz/{quiz_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json().get("title") == "Teste Simples"
