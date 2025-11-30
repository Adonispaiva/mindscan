#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
async_pipeline.py — AsyncPipeline (Pipeline 100% Assíncrona do MindScan)
------------------------------------------------------------------------

Objetivo:
- Transformar a pipeline completa do MindScan em um fluxo assíncrono real.
- Eliminar bloqueios durante as etapas de geração.
- Integrar com WeasyRendererAsync.
- Integrar SectionEngine (modo paralelo inteligente).
- Integrar Telemetria Avançada (async-safe).
- Integrar Logger corporativo.

Requisitos:
- Python 3.10+
- WeasyRendererAsync (renderer assíncrono)
- SectionEngine (gerenciamento modular das seções)
"""

import asyncio
from pathlib import Path

from backend.services.pdf.engine.section_engine import SectionEngine
from backend.services.pdf.renderers.weasy_renderer_async import WeasyRendererAsync
from backend.services.pdf.telemetry.telemetry_advanced import TelemetryAdvanced


class AsyncPipeline:

    def __init__(
        self,
        secoes,
        templates_dir: Path,
        logger=None,
        telemetry: TelemetryAdvanced = None,
        turbo: bool = False,
        max_workers: int = 6,
    ):
        """
        secoes: lista de seções da pipeline (instâncias)
        templates_dir: pasta com templates HTML/CSS do PDF
        turbo: ativa paralelização inteligente no SectionEngine
        """
        self.secoes = secoes
        self.templates_dir = Path(templates_dir)
        self.logger = logger
        self.telemetry = telemetry
        self.turbo = turbo
        self.max_workers = max_workers

        if self.logger:
            self.logger.info(
                f"AsyncPipeline inicializado. TURBO={self.turbo}, workers={self.max_workers}"
            )

        # Engines internos
        self.section_engine = SectionEngine(
            secoes=self.secoes,
            logger=self.logger,
            telemetry=self.telemetry,
            turbo=self.turbo,
            max_workers=self.max_workers,
        )

        self.renderer = WeasyRendererAsync(
            self.templates_dir,
            logger=self.logger,
            max_workers=self.max_workers
        )

    # ===================================================================
    # Construção do HTML (async)
    # ===================================================================
    async def _montar_html_async(self, ctx):
        """
        Usa o SectionEngine (que pode ser paralelo) e retorna HTML final.
        """

        if self.logger:
            self.logger.info("[AsyncPipeline] Montando HTML (async).")

        if self.telemetry:
            self.telemetry.iniciar("montagem_html_async")

        # SectionEngine executa seções (sync), então rodamos em executor
        loop = asyncio.get_event_loop()
        secoes_chunks = await loop.run_in_executor(
            None,
            self.section_engine.executar,
            ctx
        )

        # Concatenar HTML
        html_final = "".join(secoes_chunks)

        if self.telemetry:
            self.telemetry.finalizar("montagem_html_async")

        return html_final

    # ===================================================================
    # Pipeline completa
    # ===================================================================
    async def gerar_relatorio_async(
        self,
        usuario,
        resultados,
        mi,
        output_path: Path = None
    ):
        """
        Executa toda a pipeline de forma assíncrona:

        1. Montagem do HTML (async)
        2. Renderização do PDF (async)
        3. Telemetria final
        """

        nome_usuario = usuario.get("nome", "Usuário")

        if self.logger:
            self.logger.evento_pdf_iniciado(nome_usuario)

        if not output_path:
            ROOT = Path(__file__).resolve().parent
            output_path = ROOT / "relatorio_mindscan_async.pdf"

        # Início da telemetria total
        if self.telemetry:
            self.telemetry.iniciar("pipeline_total_async")
            self.telemetry.registrar_renderer("WeasyRendererAsync")

        # Criar contexto
        ctx = {"usuario": usuario, "resultados": resultados, "mi": mi}

        # 1. HTML (async)
        if self.telemetry:
            self.telemetry.iniciar("html_async")

        html = await self._montar_html_async(ctx)

        if self.telemetry:
            self.telemetry.finalizar("html_async")

        # 2. Renderização (async real)
        if self.telemetry:
            self.telemetry.iniciar("render_pdf_async")

        pdf_path = await self.renderer.render_html_to_pdf(html, output_path)

        if self.telemetry:
            self.telemetry.finalizar("render_pdf_async")
            self.telemetry.registrar_tamanho_pdf(pdf_path)
            self.telemetry.finalizar("pipeline_total_async")
            self.telemetry.exportar()

        if self.logger:
            self.logger.evento_pdf_finalizado(pdf_path)

        return pdf_path

