import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_quiz_submit_missing_data():
    response = client.post("/quiz/submit", json={})
    assert response.status_code == 422  # Unprocessable Entity

def test_quiz_submit_valid():
    payload = {
        "nome": "Teste",
        "scores": {
            "DEPRESSAO": 12,
            "ANSIEDADE": 10,
            "ESTRESSE": 14
        }
    }
    response = client.post("/quiz/submit", json=payload)
    assert response.status_code == 200
    assert "Relatório MindScan MI" in response.text
