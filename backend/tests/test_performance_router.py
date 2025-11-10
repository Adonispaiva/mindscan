# ===============================================================
#  TESTES — PERFORMANCE ROUTER
#  Projeto: MindScan — SynMind MI v2.0
#  Autor: Leo Vinci (GPT Inovexa)
#  Data: 07/11/2025
#  Função: Validar endpoint /performance/analyze (FastAPI)
# ===============================================================

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ---------------------------------------------------------------
# TESTE 1 — Sucesso na análise de performance
# ---------------------------------------------------------------
def test_analyze_performance_success():
    payload = {
        "excelencia": 85.0,
        "faturamento": 78.0,
        "scores": {"DEPRESSAO": 5, "ANSIEDADE": 6, "ESTRESSE": 4}
    }

    response = client.post("/performance/analyze", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert "quadrante" in data
    assert data["quadrante"] in ["Inspirador", "Especialista", "Promissor", "Buscador"]
    assert isinstance(data["score_performance"], float)
    assert "analise_textual" in data
    assert "RESULTADO SYNMIND PERFORMANCE" in data["analise_textual"]


# ---------------------------------------------------------------
# TESTE 2 — Payload inválido (sem campo faturamento)
# ---------------------------------------------------------------
def test_analyze_performance_missing_field():
    payload = {
        "excelencia": 90.0,
        "scores": {"DEPRESSAO": 2, "ANSIEDADE": 2, "ESTRESSE": 2}
    }

    response = client.post("/performance/analyze", json=payload)
    assert response.status_code == 422  # Pydantic validation error


# ---------------------------------------------------------------
# TESTE 3 — Comportamento em valores emocionais extremos
# ---------------------------------------------------------------
def test_analyze_performance_emotional_extremes():
    payload = {
        "excelencia": 90.0,
        "faturamento": 90.0,
        "scores": {"DEPRESSAO": 28, "ANSIEDADE": 28, "ESTRESSE": 28}
    }

    response = client.post("/performance/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Espera-se queda drástica no score
    assert data["score_performance"] < 40
    assert "Buscador" in data["quadrante"] or "Promissor" in data["quadrante"]
    assert "RESULTADO SYNMIND PERFORMANCE" in data["analise_textual"]
