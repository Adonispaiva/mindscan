import pytest
from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_login_invalid():
    response = client.post("/auth/login", json={"username": "x", "password": "y"})
    assert response.status_code == 401
