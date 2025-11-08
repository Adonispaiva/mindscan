# ===============================================================
#  TESTE AUTOMATIZADO — MI ROUTER
#  Projeto: MindScan — SynMind MI v2.0
#  Autor: Leo Vinci (GPT Inovexa)
#  Data: 07/11/2025
#  Função: Validar o endpoint /mi/generate
# ===============================================================

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ---------------------------------------------------------------
# TESTE 1 — Verifica retorno básico do endpoint /mi/generate
# ---------------------------------------------------------------
def test_generate_mi_report_success():
    payload = {
        "nome": "Emília",
        "scores": {
            "DEPRESSAO": 6,
            "ANSIEDADE": 4,
            "ESTRESSE": 8
        },
        "quadrante": "Inspirador"
    }

    response = client.post("/mi/generate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert "relatorio" in data
    assert "Mind Intelligence" in data["relatorio"]
    assert "Emília" in data["relatorio"]
    assert "Inspirador" in data["relatorio"]

# ---------------------------------------------------------------
# TESTE 2 — Falha por payload incorreto
# ---------------------------------------------------------------
def test_generate_mi_report_invalid_payload():
    # Falta o campo quadrante
    payload = {
        "nome": "Lucas",
        "scores": {
            "DEPRESSAO": 10,
            "ANSIEDADE": 7,
            "ESTRESSE": 5
        }
    }

    response = client.post("/mi/generate", json=payload)
    assert response.status_code == 422  # Unprocessable Entity
