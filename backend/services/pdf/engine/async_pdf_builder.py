# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\engine\async_pdf_builder.py
# Última atualização: 2025-12-11T09:59:21.200087

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
async_pdf_builder.py — AsyncPDFBuilder (Builder 100% Assíncrono)
-----------------------------------------------------------------

Versão final do Builder Assíncrono do MindScan PDF Engine.

Características:
- Totalmente async/await
- Integração com SectionEngine (paralelo inteligente)
- Integração com WeasyRendererAsync (PDF real)
- Integração com DistributedRenderer (modo remoto async via executor)
- Telemetria Avançada (async-safe)
- Logger Corporativo
- Chunking de HTML
- Pré-compilação de seções
"""

import asyncio
from pathlib import Path

from backend.services.pdf.engine.section_engine import SectionEngine
from backend.services.pdf.renderers.weasy_renderer_async import WeasyRendererAsync
from backend.services.pdf.renderers.distributed_renderer import DistributedRenderer
from backend.services.pdf.telemetry.telemetry_advanced import TelemetryAdvanced


class AsyncPDFBuilder:

    def __init__(
        self,
        secoes,
        templates_dir: Path,
        logger=None,
        telemetry: TelemetryAdvanced = None,
        turbo: bool = False,
        max_workers: int = 6,
        distributed_endpoint: str = None
    ):
        """
        secoes: lista de instâncias das seções
        templates_dir: pasta base dos templates HTML/CSS
        turbo: ativa paralelização inteligente
        distributed_endpoint: URL de renderização remota (opcional)
        """
        self.secoes = secoes
        self.templates_dir = Path(templates_dir)

        self.logger = logger
        self.telemetry = telemetry
        self.turbo = turbo
        self.max_workers = max_workers
        self.distributed_endpoint = distributed_endpoint

        if self.logger:
            self.logger.info(
                f"AsyncPDFBuilder inicializado. Turbo={self.turbo}, Workers={self.max_workers}"
            )

        # Engines internos
        self.section_engine = SectionEngine(
            secoes=self.secoes,
            logger=self.logger,
            telemetry=self.telemetry,
            turbo=self.turbo,
            max_workers=self.max_workers
        )

        # Renderers
        self.local_renderer = WeasyRendererAsync(
            templates_dir=self.templates_dir,
            logger=self.logger,
            max_workers=self.max_workers
        )

        self.remote_renderer = None
        if distributed_endpoint:
            # Para compatibilidade com o protótipo remoto (sync), usamos executor
            self.remote_renderer = DistributedRenderer(
                templates_dir=self.templates_dir,
                endpoint=distributed_endpoint,
                logger=self.logger,
                telemetry=self.telemetry,
                fallback_local=True
            )

    # ===================================================================
    # Montagem do HTML (async + SectionEngine paralelo)
    # ===================================================================
    async def _montar_html_async(self, usuario, resultados, mi):
        ctx = {
            "usuario": usuario,
            "resultados": resultados,
            "mi": mi
        }

        if self.logger:
            self.logger.info("[AsyncPDFBuilder] Montando HTML…")

        if self.telemetry:
            self.telemetry.iniciar("montagem_html_async")

        loop = asyncio.get_event_loop()
        chunks = await loop.run_in_executor(
            None,
            self.section_engine.executar,
            ctx
        )

        html_final = "".join(chunks)

        if self.telemetry:
            self.telemetry.finalizar("montagem_html_async")

        return html_final

    # ===================================================================
    # Renderização do PDF (async)
    # ===================================================================
    async def _renderizar_async(self, html: str, output_path: Path):
        """
        Seleciona renderer remoto → fallback local.
        """

        # Telemetria
        if self.telemetry:
            self.telemetry.iniciar("render_pdf_async")

        loop = asyncio.get_event_loop()

        # 1) Renderer remoto (se configurado)
        if self.remote_renderer:
            try:
                if self.logger:
                    self.logger.info("[AsyncPDFBuilder] Tentando render remoto async.")

                # Executar renderer remoto em executor (ele é sync)
                await loop.run_in_executor(
                    None,
                    self.remote_renderer.render_html_to_pdf,
                    html,
                    output_path
                )

                if self.logger:
                    self.logger.info("[AsyncPDFBuilder] Render remoto concluído.")

            except Exception as e:
                if self.logger:
                    self.logger.evento_erro("AsyncPDFBuilder.render_remoto", e)
                # fallback automático para local async
                await self.local_renderer.render_html_to_pdf(html, output_path)

        else:
            # 2) Renderer local assíncrono
            await self.local_renderer.render_html_to_pdf(html, output_path)

        if self.telemetry:
            self.telemetry.finalizar("render_pdf_async")

        return output_path

    # ===================================================================
    # Pipeline completa (async)
    # ===================================================================
    async def gerar_relatorio_async(
        self,
        usuario,
        resultados,
        mi,
        output_path: Path = None
    ):
        """
        Pipeline 100% async:
        1. montar HTML async
        2. renderizar PDF async
        3. registrar telemetria
        """

        nome_usuario = usuario.get("nome", "Usuário")

        if self.logger:
            self.logger.evento_pdf_iniciado(nome_usuario)

        if output_path is None:
            ROOT = Path(__file__).resolve().parent
            output_path = ROOT / "relatorio_mindscan_async.pdf"

        # telemetria total
        if self.telemetry:
            self.telemetry.iniciar("pipeline_total_async")
            self.telemetry.registrar_renderer(
                "DistributedRenderer" if self.remote_renderer else "WeasyRendererAsync"
            )

        # 1 — HTML
        if self.telemetry:
            self.telemetry.iniciar("html_async")

        html = await self._montar_html_async(usuario, resultados, mi)

        if self.telemetry:
            self.telemetry.finalizar("html_async")

        # 2 — Renderização
        pdf_path = await self._renderizar_async(html, output_path)

        # 3 — Telemetria final
        if self.telemetry:
            self.telemetry.registrar_tamanho_pdf(pdf_path)
            self.telemetry.finalizar("pipeline_total_async")
            self.telemetry.exportar()

        if self.logger:
            self.logger.evento_pdf_finalizado(pdf_path)

        return pdf_path
