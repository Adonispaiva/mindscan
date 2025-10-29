import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_submit_quiz_response(async_client: AsyncClient, auth_header):
    # Cria quiz primeiro
    quiz_data = {
        "title": "Teste Memória",
        "questions": [
            {"question": "5x5?", "options": ["20", "25"], "answer": "25"}
        ]
    }
    quiz = await async_client.post("/quiz/create", json=quiz_data, headers=auth_header)
    quiz_id = quiz.json()["quiz_id"]

    # Envia resposta
    answer_payload = {
        "quiz_id": quiz_id,
        "answers": ["25"]
    }
    response = await async_client.post("/response/submit", json=answer_payload, headers=auth_header)
    assert response.status_code == 200
    assert "score" in response.json()


@pytest.mark.asyncio
async def test_get_user_responses(async_client: AsyncClient, auth_header):
    response = await async_client.get("/response/my", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
