import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/", allow_redirects=False)
    assert response.status_code == 307
    assert "/docs" in response.headers["location"]
