import pytest
from analytics.diagnostic_engine import interpretar_dass21
from analytics.report_generator import gerar_relatorio_mi

# --------------------------------------
# 🔬 FIXTURE DE EXEMPLO (DASS SIMPLES)
# --------------------------------------
@pytest.fixture
def exemplo_scores():
    return {
        "DEPRESSAO": 6,   # NORMAL
        "ANSIEDADE": 8,   # LEVE
        "ESTRESSE": 18    # MODERADO
    }

# --------------------------------------
# ✅ TESTE: INTERPRETAÇÃO DOS SCORES
# --------------------------------------

def test_interpretar_dass21(exemplo_scores):
    resultado = interpretar_dass21(exemplo_scores)
    assert resultado["DEPRESSAO"]["nivel"] == "NORMAL"
    assert resultado["ANSIEDADE"]["nivel"] == "LEVE"
    assert resultado["ESTRESSE"]["nivel"] == "MODERADO"

# --------------------------------------
# ✅ TESTE: RELATÓRIO NARRATIVO
# --------------------------------------

def test_gerar_relatorio_mi(exemplo_scores):
    resultado = interpretar_dass21(exemplo_scores)
    relatorio = gerar_relatorio_mi(resultado, nome="Teste")

    assert "Relatório MindScan MI" in relatorio
    assert "Teste" in relatorio
    assert "NORMAL" in relatorio
    assert "LEVE" in relatorio
    assert "MODERADO" in relatorio
