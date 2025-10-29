import requests

BASE_URL = "http://localhost:8000"

def test_health_check():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"status": "API do MindScan operando normalmente."}

def test_quiz_submit():
    payload = {
        "performance": [0],
        "matcher": [0]
    }
    response = requests.post(f"{BASE_URL}/quiz/submit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "territory" in data
    assert data["territory"] == "buscadores"
