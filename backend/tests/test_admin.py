import pytest
from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_admin_dashboard():
    response = client.get("/admin/dashboard")
    assert response.status_code == 200
    assert "dashboard" in response.json()
