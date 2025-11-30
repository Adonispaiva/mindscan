#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste oficial do AsyncPDFBuilder (v43).
Cobre:
- pipeline completa assíncrona
- SectionEngine (parallel-aware)
- renderer async
- fallback remoto (mock)
- telemetria avançada
"""

import asyncio
import pytest
from pathlib import Path

from backend.services.pdf.engine.async_pdf_builder import AsyncPDFBuilder
from backend.services.pdf.telemetry.telemetry_advanced import TelemetryAdvanced


# -------------------------------------------------------------------
# FIXTURES
# -------------------------------------------------------------------
@pytest.fixture
def secoes_fake():
    """Seções mínimas para teste do AsyncPDFBuilder."""
    class FakeSection:
        def render(self, ctx):
            return "<p>OK</p>"
    return [FakeSection(), FakeSection()]


@pytest.fixture
def templates_dir(tmp_path):
    """Templates HTML/CSS fake para testes."""
    base = tmp_path / "base.html"
    css = tmp_path / "estilo.css"

    base.write_text("<html><body>{{conteudo}}</body></html>", encoding="utf-8")
    css.write_text("body { font-size: 12px; }", encoding="utf-8")

    return tmp_path


@pytest.fixture
def telemetry(tmp_path):
    log_dir = tmp_path / "logs"
    log_dir.mkdir(exist_ok=True)
    return TelemetryAdvanced(log_dir)


@pytest.fixture
def logger():
    class FakeLogger:
        def info(self, msg): pass
        def warn(self, msg): pass
        def error(self, msg): pass
        def evento_pdf_iniciado(self, msg): pass
        def evento_pdf_finalizado(self, msg): pass
        def evento_erro(self, f, e): pass
    return FakeLogger()


# -------------------------------------------------------------------
# TESTE PRINCIPAL — AsyncPDFBuilder
# -------------------------------------------------------------------
@pytest.mark.asyncio
async def test_async_pdf_builder_end_to_end(
    secoes_fake,
    templates_dir,
    telemetry,
    logger,
    tmp_path
):
    output = tmp_path / "builder_async.pdf"

    builder = AsyncPDFBuilder(
        secoes=secoes_fake,
        templates_dir=templates_dir,
        logger=logger,
        telemetry=telemetry,
        turbo=False,
        max_workers=2
    )

    pdf_path = await builder.gerar_relatorio_async(
        usuario={"nome": "Teste"},
        resultados={},
        mi={},
        output_path=output
    )

    # Verificações essenciais
    assert pdf_path.exists(), "O PDF deveria ter sido criado pelo AsyncPDFBuilder."
    assert pdf_path.stat().st_size > 0, "O PDF final não pode ser vazio."

    # Telemetria deve existir
    telemetry_file = telemetry.telemetry_file
    assert telemetry_file.exists(), "O arquivo de telemetria deveria existir."
    assert telemetry_file.stat().st_size > 0, "A telemetria não deveria estar vazia."
