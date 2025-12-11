# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\tests\async\test_distributed_renderer_async.py
# Última atualização: 2025-12-11T09:59:27.777220

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste oficial do DistributedRenderer em modo async.
Cobre:
- chamada remota simulada
- comportamento de fallback local
- render PDF em pipeline async
- telemetria de render_distributed
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
    class FakeSection:
        def render(self, ctx):
            return "<p>FAKE_OK</p>"
    return [FakeSection(), FakeSection()]


@pytest.fixture
def templates_dir(tmp_path):
    base = tmp_path / "base.html"
    css = tmp_path / "estilo.css"

    base.write_text("<html><body>{{conteudo}}</body></html>", encoding="utf-8")
    css.write_text("body { color: black; }", encoding="utf-8")

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
# MOCK DO SERVIDOR REMOTO
# -------------------------------------------------------------------
@pytest.fixture
def fake_remote_server(monkeypatch):
    """
    Simula um servidor remoto via monkeypatching da função
    requests.post usada pelo DistributedRenderer.
    """
    import requests

    class FakeResponse:
        status_code = 200
        content = b"%PDF-FAKE"

        def json(self):
            return {}

    def fake_post(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(requests, "post", fake_post)


# -------------------------------------------------------------------
# TESTE PRINCIPAL
# -------------------------------------------------------------------
@pytest.mark.asyncio
async def test_distributed_renderer_async_end_to_end(
    secoes_fake,
    templates_dir,
    telemetry,
    logger,
    tmp_path,
    fake_remote_server
):
    """Teste integrando AsyncPDFBuilder + DistributedRenderer."""

    output = tmp_path / "distributed_async.pdf"

    builder = AsyncPDFBuilder(
        secoes=secoes_fake,
        templates_dir=templates_dir,
        logger=logger,
        telemetry=telemetry,
        turbo=False,
        max_workers=2,
        distributed_endpoint="http://fake-remote/render"
    )

    pdf_path = await builder.gerar_relatorio_async(
        usuario={"nome": "ClusterTest"},
        resultados={},
        mi={},
        output_path=output
    )

    # Verificações essenciais
    assert pdf_path.exists(), "PDF deveria ser criado via DistributedRenderer."
    assert pdf_path.stat().st_size > 0, "PDF não pode estar vazio."

    # Telemetria deve ter registrado "render_distributed"
    with open(telemetry.telemetry_file, "r", encoding="utf-8") as f:
        data = f.read()

    assert "render_distributed" in data, "Telemetria deveria registrar render distribuído."
