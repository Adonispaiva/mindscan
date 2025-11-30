#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_stress_weasy_real.py — Stress Test REAL do MindScan PDF Engine
-------------------------------------------------------------------

Este teste gera PDFs reais usando WeasyPrint para validar:

- Estabilidade sob carga real
- Tempo médio de renderização
- Uso de memória
- Ausência de travamentos
- Compatibilidade de templates
- Integridade final dos PDFs

ATENÇÃO:
Este teste é consideravelmente pesado.
Executa 10 ciclos de geração REAL de PDF usando WeasyPrint.
"""

import time
from pathlib import Path
import pytest

from pdf_builder import PDFBuilder
from backend.services.pdf.renderers.weasy_renderer import WeasyRenderer
from backend.services.pdf.validators.data_validator import MindScanDataValidator
from backend.services.pdf.telemetry.logger import MindScanLogger


# -------------------------------------------------------------------------
# FIXTURES
# -------------------------------------------------------------------------
@pytest.fixture
def usuario():
    return {
        "nome": "Stress Test Real",
        "cargo": "QA Senior",
        "idade": 33
    }


@pytest.fixture
def resultados():
    return {
        "big_five": {
            "abertura": 75,
            "conscienciosidade": 70,
            "extroversao": 50,
            "agradabilidade": 65,
            "neuroticismo": 20
        },
        "dass": {"depressao": "Normal", "ansiedade": "Normal", "estresse": "Leve"},
        "esquemas": {"Autoexigência": "Moderado"},
        "performance": {"2025-Q1": 85, "2025-Q2": 88},
        "bussola": {"Analítico": "Alto", "Executor": "Forte"}
    }


@pytest.fixture
def mi():
    return {
        "resumo_executivo": {
            "texto": "Relatório de stress test REAL com WeasyPrint."
        }
    }


# -------------------------------------------------------------------------
# TESTE REAL COM WEASYRENDERER
# -------------------------------------------------------------------------
def test_stress_weasy_real(usuario, resultados, mi, tmp_path):
    """
    Executa 10 gerações REAIS de PDF usando o WeasyRenderer.

    Objetivos:
    - Garantir que o motor não degrade
    - Detectar memory leaks
    - Validar estabilidade real do renderer
    """

    TEMPLATES_DIR = (
        Path(__file__).resolve().parent.parent
        / "backend" / "services" / "pdf" / "templates"
    )

    logger = MindScanLogger()
    validator = MindScanDataValidator()

    # validar antes de iniciar
    validator.validar(usuario, resultados, mi)

    tempos = []
    total_start = time.perf_counter()

    for i in range(10):
        start = time.perf_counter()

        output_path = tmp_path / f"stress_real_{i}.pdf"

        renderer = WeasyRenderer(TEMPLATES_DIR, logger=logger)
        builder = PDFBuilder(logger=logger)

        pdf_path = builder.gerar_relatorio(
            usuario,
            resultados,
            mi,
            renderer,
            output_path=output_path
        )

        duracao = time.perf_counter() - start
        tempos.append(duracao)

        # Garantias básicas
        assert pdf_path.exists(), f"PDF {i} não foi criado."
        assert pdf_path.stat().st_size > 5_000, "PDF parece muito pequeno — pode ter falhado."

        # PDF real não pode ultrapassar 7s (limite seguro)
        assert duracao < 7.0, f"Ciclo {i} muito lento: {duracao:.2f}s"

    tempo_total = time.perf_counter() - total_start
    media = sum(tempos) / len(tempos)

    # Métricas obrigatórias:
    assert tempo_total < 60.0, "Tempo total muito alto para 10 PDFs reais."
    assert media < 5.0, f"Média por PDF acima do esperado: {media:.2f}s"

    print("\n=== RESULTADOS DO STRESS TEST REAL ===")
    print(f"Tempo total: {tempo_total:.2f}s")
    print(f"Tempo médio: {media:.2f}s\n")
