import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_user_validation():
    response = client.post("/users/create", json={"email": "invalid"})
    assert response.status_code == 422

def test_create_user_valid():
    user_data = {
        "email": "user@example.com",
        "password": "12345678"
    }
    response = client.post("/users/create", json=user_data)
    assert response.status_code in [200, 201]
