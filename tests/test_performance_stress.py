#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_performance_stress.py — Testes de Stress e Performance do MindScan PDF Engine
---------------------------------------------------------------------------------

Objetivos:
- Garantir que a montagem do HTML não ultrapasse limites de tempo
- Validar desempenho sob múltiplos ciclos de geração (stress test)
- Medir tempo médio por ciclo
- Detectar regressões de performance no PDFBuilder

Observação:
- Não gera PDF real (usa renderer mock)
"""

import time
import pytest
from pathlib import Path

from pdf_builder import PDFBuilder
from backend.services.pdf.validators.data_validator import MindScanDataValidator


# -------------------------------------------------------------------------
# FIXTURES REUTILIZADAS
# -------------------------------------------------------------------------
@pytest.fixture
def usuario():
    return {
        "nome": "Teste Stress",
        "cargo": "QA",
        "idade": 30
    }


@pytest.fixture
def resultados():
    return {
        "big_five": {
            "abertura": 70,
            "conscienciosidade": 60,
            "extroversao": 40,
            "agradabilidade": 55,
            "neuroticismo": 30,
        },
        "dass": {"depressao": "Normal", "ansiedade": "Leve", "estresse": "Moderado"},
        "esquemas": {"Autoexigência": "Moderado"},
        "performance": {"2024-Q1": 80, "2024-Q2": 82},
        "bussola": {"Analítico": "Alto", "Executor": "Forte"},
    }


@pytest.fixture
def mi():
    return {"resumo_executivo": {"texto": "Stress test ativo."}}


# -------------------------------------------------------------------------
# RENDERER MOCK (EXTREMAMENTE RÁPIDO)
# -------------------------------------------------------------------------
class RendererMock:
    def render_html_to_pdf(self, html: str, output_path: Path):
        output_path.write_text("PDF_FAKE", encoding="utf-8")
        return output_path


# -------------------------------------------------------------------------
# TESTE 1: Performance da montagem do HTML
# -------------------------------------------------------------------------
def test_html_performance(usuario, resultados, mi, tmp_path):
    """
    A montagem do HTML deve executar rapidamente (< 0.5s em média).
    """

    builder = PDFBuilder()
    start = time.perf_counter()

    html = builder._montar_html(usuario, resultados, mi)

    duracao = time.perf_counter() - start

    # HTML deve ser gerado corretamente
    assert "<section" in html.lower()

    # Performance mínima obrigatória
    assert duracao < 0.5, f"Montagem HTML muito lenta: {duracao:.4f}s"


# -------------------------------------------------------------------------
# TESTE 2: Stress test — 50 ciclos consecutivos
# -------------------------------------------------------------------------
def test_stress_50_ciclos(usuario, resultados, mi, tmp_path):
    """
    Executa 50 ciclos completos de geração simulada.
    Nenhum ciclo pode exceder 1 segundo.
    """

    builder = PDFBuilder()
    renderer = RendererMock()

    tempos = []

    for i in range(50):
        start = time.perf_counter()
        pdf_path = tmp_path / f"stress_{i}.pdf"

        builder.gerar_relatorio(
            usuario,
            resultados,
            mi,
            renderer,
            output_path=pdf_path
        )

        dur = time.perf_counter() - start
        tempos.append(dur)

        assert dur < 1.0, f"Ciclo {i} muito lento: {dur:.4f}s"

    # Média deve ser extremamente rápida
    media = sum(tempos) / len(tempos)
    assert media < 0.25, f"Média de ciclos muito lenta: {media:.4f}s"


# -------------------------------------------------------------------------
# TESTE 3: Stress extremo — 200 montagens de HTML
# -------------------------------------------------------------------------
def test_stress_extremo_html(usuario, resultados, mi):
    """
    Testa robustez do builder somente para montagem de HTML.
    Deve suportar 200 montagens sem queda brusca de performance.
    """

    builder = PDFBuilder()
    total_start = time.perf_counter()

    for _ in range(200):
        html = builder._montar_html(usuario, resultados, mi)
        assert "<section" in html.lower()

    duracao_total = time.perf_counter() - total_start

    # limite: 200 montagens não podem ultrapassar 5 segundos
    assert duracao_total < 5.0, f"Stress HTML excedeu limite: {duracao_total:.2f}s"


# -------------------------------------------------------------------------
# TESTE 4: Validação rápida sob alta carga (100 ciclos)
# -------------------------------------------------------------------------
def test_validacao_stress(usuario, resultados, mi):
    validator = MindScanDataValidator()

    start = time.perf_counter()

    for _ in range(100):
        assert validator.validar(usuario, resultados, mi) is True

    duracao = time.perf_counter() - start
    assert duracao < 1.0, f"Validação muito lenta: {duracao:.4f}s"
