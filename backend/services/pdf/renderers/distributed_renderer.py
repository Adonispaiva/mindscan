#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
distributed_renderer.py — DistributedRenderer (Protótipo Cluster Inovexa)
-------------------------------------------------------------------------

Objetivo:
- Enviar HTML + CSS para um servidor remoto que gera o PDF.
- Retornar o PDF final para o PDFBuilder.
- Permitir renderização distribuída (cluster de render nodes).
- Integrar com Logger e Telemetria Avançada.
- Oferecer fallback automático para render local (WeasyRenderer).

Modo de operação:
- Envia requisição POST para /render
- Payload: { html, base_url }
- Retorno: PDF em bytes
"""

import requests
from pathlib import Path
from backend.services.pdf.renderers.weasy_renderer import WeasyRenderer


class DistributedRenderer:

    def __init__(
        self,
        templates_dir: Path,
        endpoint: str,
        logger=None,
        telemetry=None,
        timeout: int = 20,
        fallback_local: bool = True
    ):
        """
        templates_dir: pasta contendo base.html e estilo.css (para o fallback)
        endpoint: URL do servidor remoto (ex: http://10.0.0.25:5000/render)
        fallback_local: se True, usa WeasyRenderer em caso de falha
        """
        self.templates_dir = Path(templates_dir)
        self.endpoint = endpoint
        self.logger = logger
        self.telemetry = telemetry
        self.timeout = timeout
        self.fallback_local = fallback_local

        self.local_renderer = WeasyRenderer(templates_dir, logger=logger)

        if self.logger:
            self.logger.info(
                f"DistributedRenderer inicializado. Endpoint={endpoint}, "
                f"fallback_local={fallback_local}"
            )

    # ----------------------------------------------------------------------
    # Envio ao servidor remoto
    # ----------------------------------------------------------------------
    def _render_remoto(self, html: str):
        """
        Envia HTML para o servidor remoto e recebe PDF (bytes).
        """

        try:
            if self.logger:
                self.logger.info(f"[DistributedRenderer] Enviando job para {self.endpoint}")

            response = requests.post(
                self.endpoint,
                json={"html": html, "base_url": str(self.templates_dir)},
                timeout=self.timeout,
            )

            if response.status_code != 200:
                raise RuntimeError(
                    f"Falha no servidor remoto ({response.status_code}): {response.text}"
                )

            return response.content  # PDF em bytes

        except Exception as e:
            if self.logger:
                self.logger.evento_erro("DistributedRenderer._render_remoto", e)
            raise e

    # ----------------------------------------------------------------------
    # Método principal
    # ----------------------------------------------------------------------
    def render_html_to_pdf(self, html: str, output_path: Path):
        """
        Tenta renderizar remotamente.
        Caso falhe, faz fallback para render local.
        """

        # Telemetria
        if self.telemetry:
            self.telemetry.iniciar("render_distributed")

        try:
            # 1. Tentar render remoto
            pdf_bytes = self._render_remoto(html)

            # 2. Salvar PDF recebido
            with open(output_path, "wb") as f:
                f.write(pdf_bytes)

            if self.logger:
                self.logger.info("[DistributedRenderer] PDF gerado remotamente com sucesso.")

        except Exception:
            # Fallback automático
            if self.fallback_local:
                if self.logger:
                    self.logger.warn("[DistributedRenderer] Falha remota. Usando fallback local.")
                output_path = self.local_renderer.render_html_to_pdf(html, output_path)
            else:
                raise

        if self.telemetry:
            self.telemetry.finalizar("render_distributed")

        return output_path
