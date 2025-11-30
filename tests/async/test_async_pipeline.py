#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste oficial do AsyncPipeline do MindScan.
Cobre:
- montagem async de HTML
- integração com SectionEngine paralelo
- renderização PDF async (mock)
- telemetria
"""

import asyncio
import pytest
from pathlib import Path

from backend.services.pdf.engine.async_pipeline import AsyncPipeline
from backend.services.pdf.renderers.weasy_renderer_async import WeasyRendererAsync
from backend.services.pdf.telemetry.telemetry_advanced import TelemetryAdvanced
from backend.services.pdf.engine.section_engine import SectionEngine


# -------------------------------------------------------------------
# FIXTURES
# -------------------------------------------------------------------
@pytest.fixture
def secoes_fake():
    """Seções mínimas para teste async."""
    class FakeSection:
        def render(self, ctx):
            return "<div>OK</div>"
    return [FakeSection(), FakeSection()]


@pytest.fixture
def templates_dir(tmp_path):
    """Cria templates fake."""
    base = tmp_path / "base.html"
    css = tmp_path / "estilo.css"

    base.write_text("<html><body>{{conteudo}}</body></html>", encoding="utf-8")
    css.write_text("body { font-family: Arial; }", encoding="utf-8")

    return tmp_path


@pytest.fixture
def telemetry(tmp_path):
    logs = tmp_path / "logs"
    logs.mkdir(exist_ok=True)
    return TelemetryAdvanced(logs)


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
# TESTE PRINCIPAL
# -------------------------------------------------------------------
@pytest.mark.asyncio
async def test_async_pipeline_end_to_end(secoes_fake, templates_dir, telemetry, logger, tmp_path):
    """
    Executa:
    - AsyncPipeline
    - SectionEngine (modo TURBO off)
    - Renderer async real (WeasyRendererAsync)
    """

    output = tmp_path / "teste_async.pdf"

    pipeline = AsyncPipeline(
        secoes=secoes_fake,
        templates_dir=templates_dir,
        logger=logger,
        telemetry=telemetry,
        turbo=False,
        max_workers=2
    )

    path = await pipeline.gerar_relatorio_async(
        usuario={"nome": "Teste"},
        resultados={},
        mi={},
        output_path=output
    )

    assert path.exists(), "O PDF deveria ter sido criado."
    assert path.stat().st_size > 0, "O PDF gerado não pode estar vazio."

    # Verificação mínima do HTML gerado
    # (não valida conteúdo real, pois é um mock)
    with open(path, "rb") as f:
        data = f.read()
    assert len(data) > 10
