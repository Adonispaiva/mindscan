import pytest
from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_api_root():
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"message": "API funcionando"}
