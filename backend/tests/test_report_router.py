# ===============================================================
#  TESTES — REPORT ROUTER
#  Projeto: MindScan — SynMind MI v2.0
#  Autor: Leo Vinci (GPT Inovexa)
#  Data: 07/11/2025
#  Função: Validar endpoint /report/generate e PDF retornado
# ===============================================================

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ---------------------------------------------------------------
# TESTE 1 — Geração de relatório PDF bem-sucedida
# ---------------------------------------------------------------
def test_generate_report_success(tmp_path):
    payload = {
        "nome": "Emília Teste",
        "scores": {"DEPRESSAO": 5, "ANSIEDADE": 4, "ESTRESSE": 7},
        "quadrante": "Inspirador",
        "score_performance": 82.5,
        "relatorio_mi": "Texto interpretativo de teste para o relatório SynMind."
    }

    response = client.post("/report/generate", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment; filename=Relatorio_MindScan_Emília_Teste.pdf" in response.headers["content-disposition"]

    # Salva o PDF em tmp_path para verificação offline
    pdf_file = tmp_path / "Relatorio_MindScan_Teste.pdf"
    with open(pdf_file, "wb") as f:
        f.write(response.content)

    assert pdf_file.exists()
    # Verifica se há assinatura institucional no conteúdo
    assert b"MindScan" in response.content
    assert b"SynMind" in response.content


# ---------------------------------------------------------------
# TESTE 2 — Falha por payload incompleto
# ---------------------------------------------------------------
def test_generate_report_missing_field():
    payload = {
        "nome": "Lucas",
        # Faltam campos essenciais (scores, quadrante, etc.)
    }
    response = client.post("/report/generate", json=payload)
    assert response.status_code == 422  # Validação Pydantic


# ---------------------------------------------------------------
# TESTE 3 — Validação de tipo de arquivo
# ---------------------------------------------------------------
def test_generate_report_filetype():
    payload = {
        "nome": "Joana",
        "scores": {"DEPRESSAO": 8, "ANSIEDADE": 6, "ESTRESSE": 9},
        "quadrante": "Buscador",
        "score_performance": 61.0,
        "relatorio_mi": "Relatório narrativo de validação."
    }

    response = client.post("/report/generate", json=payload)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")
