#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
weasy_renderer_async.py — Renderer Assíncrono Experimental do MindScan PDF Engine
-------------------------------------------------------------------------------

Objetivo:
- Executar a renderização com WeasyPrint de forma assíncrona.
- Evitar bloqueio da thread principal em servidores concorrentes.
- Integrar com o modo TURBO + pipeline otimizada do PDFBuilder v36.
- Manter compatibilidade com logger + telemetria.

Estratégia:
- WeasyPrint NÃO é nativamente async.
- Uso correto: delegar a renderização para ThreadPoolExecutor.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from weasyprint import HTML, CSS


class WeasyRendererAsync:

    def __init__(self, templates_dir: Path, logger=None, max_workers: int = 4):
        """
        templates_dir: pasta contendo base.html e estilo.css
        max_workers: número máximo de threads para execução paralela
        """
        self.templates_dir = Path(templates_dir)
        self.logger = logger
        self.max_workers = max_workers

        self.base_html = self.templates_dir / "base.html"
        self.css_file = self.templates_dir / "estilo.css"

        # Executor assíncrono
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)

        # Logs iniciais
        if self.logger:
            self.logger.info(f"WeasyRendererAsync inicializado com {self.max_workers} threads.")

        # Validação dos templates
        if not self.base_html.exists():
            msg = f"Template base não encontrado: {self.base_html}"
            if self.logger: self.logger.error(msg)
            raise FileNotFoundError(msg)

        if not self.css_file.exists():
            msg = f"Arquivo de estilo não encontrado: {self.css_file}"
            if self.logger: self.logger.error(msg)
            raise FileNotFoundError(msg)

    # ----------------------------------------------------------------------
    # OPERADOR ASSÍNCRONO PRINCIPAL
    # ----------------------------------------------------------------------
    async def render_html_to_pdf(self, conteudo_html: str, output_path: Path):
        """
        Método realmente assíncrono.
        Despacha a renderização para um pool de threads.
        """

        loop = asyncio.get_event_loop()

        if self.logger:
            self.logger.info("Renderização assíncrona iniciada (WeasyRendererAsync).")
            self.logger.info(f"Arquivo destino: {output_path}")

        try:
            # Carregar template base
            base = self.base_html.read_text(encoding="utf-8")
            final_html = base.replace("{{conteudo}}", conteudo_html)

            # Execução real da renderização (não-bloqueante)
            await loop.run_in_executor(
                self.executor,
                self._render_sync,      # função síncrona abaixo
                final_html,
                output_path
            )

            if self.logger:
                self.logger.info("Renderização assíncrona concluída com sucesso.")

            return output_path

        except Exception as e:
            if self.logger:
                self.logger.evento_erro("WeasyRendererAsync.render_html_to_pdf", e)
            raise e

    # ----------------------------------------------------------------------
    # Função síncrona chamada dentro do executor
    # ----------------------------------------------------------------------
    def _render_sync(self, html_str: str, output_path: Path):
        """
        Função SÍNCRONA que realiza a renderização real.
        Executada dentro do ThreadPoolExecutor.
        """
        HTML(string=html_str, base_url=str(self.templates_dir)).write_pdf(
            str(output_path),
            stylesheets=[CSS(filename=str(self.css_file))]
        )
