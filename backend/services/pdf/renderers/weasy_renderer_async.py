#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
weasy_renderer_async.py — Renderer Assíncrono WeasyPrint (MindScan v2.0)
Autor: Leo Vinci (Inovexa)
-------------------------------------------------------------------------------
FINALIDADE:
    - Executar renderização PDF de forma **assíncrona**
    - Compatível com ReportEngine v2.0
    - Compatível com PDFEngine v2.0
    - Compatível com AsyncPDFPipeline v2.0
    - NÃO usa base.html
    - NÃO injeta {{conteudo}}
    - Recebe HTML FINAL já montado
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from weasyprint import HTML, CSS


class WeasyRendererAsync:
    """
    Renderer assíncrono oficial do MindScan v2.0.
    """

    def __init__(self, logger=None, max_workers: int = 4):
        self.logger = logger
        self.max_workers = max_workers

        # Executor compartilhado
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

        if self.logger:
            self.logger.info(
                f"WeasyRendererAsync v2.0 inicializado (threads={max_workers})."
            )

    # ----------------------------------------------------------------------
    # MÉTODO PRINCIPAL — assinatura padronizada
    # ----------------------------------------------------------------------
    async def render(self, html_final: str, css_text: str, output_path: Path):
        """
        html_final: HTML final gerado pelo ReportEngine
        css_text: conteúdo completo do CSS consolidado
        output_path: caminho onde o PDF será gravado
        """

        loop = asyncio.get_event_loop()

        if self.logger:
            self.logger.info("Renderização assíncrona iniciada (WeasyRendererAsync).")
            self.logger.info(f"Arquivo destino: {output_path}")

        try:
            css_obj = CSS(string=css_text)

            # Execução real dentro do executor
            await loop.run_in_executor(
                self.executor,
                self._render_sync,
                html_final,
                css_obj,
                output_path
            )

            if self.logger:
                self.logger.info("Renderização assíncrona concluída com sucesso.")

            return output_path

        except Exception as e:
            if self.logger:
                self.logger.evento_erro("WeasyRendererAsync.render", e)
            raise e

    # ----------------------------------------------------------------------
    # Função síncrona utilizada dentro do executor
    # ----------------------------------------------------------------------
    def _render_sync(self, html_final: str, css_obj: CSS, output_path: Path):
        HTML(string=html_final).write_pdf(
            str(output_path),
            stylesheets=[css_obj]
        )
