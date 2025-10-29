import requests

BASE_URL = "http://localhost:8000"

def test_quiz_submit():
    payload = {
        "performance": [0],
        "matcher": [0]
    }
    response = requests.post(f"{BASE_URL}/quiz/submit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["territory"] == "buscadores"
    assert "performance" in data
    assert "matcher" in data
    assert "insights" in data
