# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\renderers\distributed_renderer.py
# Última atualização: 2025-12-11T09:59:21.231327

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
distributed_renderer.py — DistributedRenderer (MindScan Cluster v2.0)
Autor: Leo Vinci (Inovexa)
---------------------------------------------------------------------------
Função:
    - Enviar HTML FINAL + CSS para servidor remoto de renderização
    - Receber PDF em bytes
    - Aplicar fallback automático usando WeasyRenderer
Compatível com:
    - ReportEngine v2.0
    - PDFBuilder v2.0
    - renderers premium, executive, technical, psychodynamic
"""

import requests
from pathlib import Path

from backend.services.pdf.renderers.weasy_renderer import WeasyRenderer


class DistributedRenderer:
    """
    Renderer distribuído oficial (SynMind / Inovexa v2.0).
    """

    def __init__(
        self,
        endpoint: str,
        logger=None,
        telemetry=None,
        timeout: int = 20,
        fallback_local: bool = True
    ):
        self.endpoint = endpoint
        self.logger = logger
        self.telemetry = telemetry
        self.timeout = timeout
        self.fallback_local = fallback_local

        # Renderer local (WeasyPrint) — versão modernizada
        self.local_renderer = WeasyRenderer(logger=logger)

        if self.logger:
            self.logger.info(
                f"DistributedRenderer v2.0 ativo. Endpoint={endpoint}, "
                f"fallback_local={fallback_local}"
            )

    # ------------------------------------------------------------------
    # Render remoto
    # ------------------------------------------------------------------
    def _render_remote(self, html_final: str, css_text: str) -> bytes:
        """
        Envia HTML FINAL + CSS para o servidor remoto de renderização.
        O servidor deve devolver PDF em bytes.
        """

        try:
            if self.logger:
                self.logger.info(
                    f"[DistributedRenderer] Enviando render job remoto → {self.endpoint}"
                )

            response = requests.post(
                self.endpoint,
                json={
                    "html": html_final,
                    "css": css_text,
                },
                timeout=self.timeout
            )

            if response.status_code != 200:
                raise RuntimeError(
                    f"Servidor remoto retornou {response.status_code}: {response.text}"
                )

            return response.content  # PDF em bytes

        except Exception as e:
            if self.logger:
                self.logger.evento_erro("DistributedRenderer._render_remote", e)
            raise e

    # ------------------------------------------------------------------
    # Método principal (assinatura padronizada v2.0)
    # ------------------------------------------------------------------
    def render(self, html_final: str, css_text: str, output_path: Path):
        """
        html_final: HTML final produzido pelo ReportEngine
        css_text: CSS consolidado
        output_path: caminho para salvar PDF
        """

        # Telemetria
        if self.telemetry:
            self.telemetry.iniciar("render_distributed")

        try:
            # 1. Tentar renderização remota (principal)
            pdf_bytes = self._render_remote(html_final, css_text)

            # 2. Salvar PDF remoto
            with open(output_path, "wb") as f:
                f.write(pdf_bytes)

            if self.logger:
                self.logger.info("[DistributedRenderer] PDF remoto gerado com sucesso.")

        except Exception:
            # 3. Fallback (WeasyRenderer)
            if self.fallback_local:
                if self.logger:
                    self.logger.warn(
                        "[DistributedRenderer] Falha remota → fallback local (WeasyRenderer)"
                    )
                return self.local_renderer.render(html_final, css_text, output_path)

            raise

        finally:
            if self.telemetry:
                self.telemetry.finalizar("render_distributed")

        return output_path
