# ===============================================================
#  TESTES — PERFORMANCE MATCHER
#  Projeto: MindScan — SynMind MI v2.0
#  Autor: Leo Vinci (GPT Inovexa)
#  Data: 07/11/2025
#  Objetivo: Validar cálculo de quadrantes e score de performance
# ===============================================================

import math
import pytest
from backend.modules.performance_matcher import calcular_matcher, gerar_analise_performance


def approx_equal(a: float, b: float, tol: float = 1e-2) -> bool:
    return abs(a - b) <= tol


# ----------------------------
# Quadrante: INSPIRADOR
# ----------------------------
def test_quadrante_inspirador():
    dados = {
        "excelencia": 80.0,
        "faturamento": 80.0,
        "scores": {"DEPRESSAO": 0, "ANSIEDADE": 0, "ESTRESSE": 0},  # emocional = 100%
    }
    res = calcular_matcher(dados)
    assert res["quadrante"] == "Inspirador"
    # score = (80*0.6 + 80*0.4) * 1.00 = 80
    assert approx_equal(res["score_performance"], 80.0)


# ----------------------------
# Quadrante: ESPECIALISTA
# ----------------------------
def test_quadrante_especialista():
    dados = {
        "excelencia": 85.0,   # >= 70
        "faturamento": 60.0,  # < 70
        "scores": {"DEPRESSAO": 2, "ANSIEDADE": 3, "ESTRESSE": 4},  # emocional ~ 100%
    }
    res = calcular_matcher(dados)
    assert res["quadrante"] == "Especialista"
    # score base = 85*0.6 + 60*0.4 = 51 + 24 = 75 (ajustado por emocional ~1.00)
    assert approx_equal(res["score_performance"], 75.0)


# ----------------------------
# Quadrante: PROMISSOR
# ----------------------------
def test_quadrante_promissor():
    dados = {
        "excelencia": 60.0,   # < 70
        "faturamento": 75.0,  # >= 70
        "scores": {"DEPRESSAO": 1, "ANSIEDADE": 1, "ESTRESSE": 1},  # emocional ~ 100%
    }
    res = calcular_matcher(dados)
    assert res["quadrante"] == "Promissor"
    # score base = 60*0.6 + 75*0.4 = 36 + 30 = 66
    assert approx_equal(res["score_performance"], 66.0)


# ----------------------------
# Quadrante: BUSCADOR
# ----------------------------
def test_quadrante_buscador():
    dados = {
        "excelencia": 50.0,
        "faturamento": 40.0,
        "scores": {"DEPRESSAO": 0, "ANSIEDADE": 0, "ESTRESSE": 0},
    }
    res = calcular_matcher(dados)
    assert res["quadrante"] == "Buscador"
    # score base = 50*0.6 + 40*0.4 = 30 + 16 = 46
    assert approx_equal(res["score_performance"], 46.0)


# ----------------------------
# Impacto do fator emocional
# ----------------------------
def test_fator_emocional_reduz_score():
    dados_ok = {
        "excelencia": 80.0,
        "faturamento": 80.0,
        "scores": {"DEPRESSAO": 0, "ANSIEDADE": 0, "ESTRESSE": 0},  # emocional = 100%
    }
    dados_ruim = {
        "excelencia": 80.0,
        "faturamento": 80.0,
        # valores altos → emocional cai (~30.7%)
        "scores": {"DEPRESSAO": 21, "ANSIEDADE": 21, "ESTRESSE": 21},
    }

    res_ok = calcular_matcher(dados_ok)
    res_ruim = calcular_matcher(dados_ruim)

    assert res_ok["score_performance"] > res_ruim["score_performance"]

    # Cálculo esperado aproximado para caso ruim:
    # emocional = 100 - ((21+21+21)/3) * 3.3 = 100 - 21*3.3 = 30.7 %
    # score = 80 * 0.307 = 24.56 (arredondado para 24.56)
    assert approx_equal(res_ruim["score_performance"], 24.56)


# ----------------------------
# Geração de análise textual
# ----------------------------
def test_gerar_analise_performance_texto():
    res = {
        "quadrante": "Inspirador",
        "score_performance": 80.0,
        "comentario": "Alta excelência e alta entrega.",
    }
    texto = gerar_analise_performance(res)
    assert "Quadrante: Inspirador" in texto
    assert "Score Geral de Performance: 80.0%" in texto
    assert "Alta excelência e alta entrega." in texto
