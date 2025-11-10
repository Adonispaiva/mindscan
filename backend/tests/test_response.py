import pytest
from backend.analytics.diagnostic_engine import interpretar_dass21
from backend.analytics.report_generator import gerar_relatorio_mi

def test_response_generation():
    scores = {"DEPRESSAO": 10, "ANSIEDADE": 15, "ESTRESSE": 20}
    interpretado = interpretar_dass21(scores)
    relatorio = gerar_relatorio_mi(interpretado, nome="Paciente X")
    
    assert "Paciente X" in relatorio
    assert any(n in relatorio for n in ["LEVE", "MODERADO", "SEVERO"])
