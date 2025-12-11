# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\pdf\engine\pdf.engine.py
# Última atualização: 2025-12-11T09:59:21.200087

# -*- coding: utf-8 -*-
"""
pdf_engine.py — MindScan SynMind v2.0
Engine de Orquestração de Renderização PDF
Autor: Leo Vinci (Inovexa)
---------------------------------------------------------------------------
Função:
    - Selecionar o renderer (Weasy, ReportLab, Distributed)
    - Enviar HTML final + CSS para o renderer
    - Monitorar recursos e instrumentar telemetria
    - Persistir o PDF final
"""

from pathlib import Path
from typing import Optional

from ..renderers.weasy_renderer import WeasyRenderer
from ..renderers.weasy_renderer_async import WeasyRendererAsync
from ..renderers.reportlab_renderer import ReportLabRenderer
from ..renderers.distributed_renderer import DistributedRenderer

from ..telemetry.logger import PDFLogger
from ..telemetry.resource_monitor import ResourceMonitor


class PDFEngine:
    """
    Engine simples e robusto.
    Responsável apenas por:
        - selecionar renderer
        - enviar HTML+CSS
        - gerar PDF final
    """

    def __init__(
        self,
        renderer: str = "weasy",
        async_mode: bool = False,
        distributed_endpoint: Optional[str] = None
    ):
        self.renderer = renderer
        self.async_mode = async_mode
        self.distributed_endpoint = distributed_endpoint

        self.logger = PDFLogger()
        self.resources = ResourceMonitor()

    # -----------------------------------------------------------
    # 1. Escolha do Renderer
    # -----------------------------------------------------------
    def _get_renderer(self):
        if self.renderer == "reportlab":
            return ReportLabRenderer(logger=self.logger)

        if self.renderer == "distributed":
            return DistributedRenderer(
                endpoint=self.distributed_endpoint,
                logger=self.logger,
                telemetry=self.resources
            )

        if self.async_mode:
            return WeasyRendererAsync(logger=self.logger)

        return WeasyRenderer(logger=self.logger)

    # -----------------------------------------------------------
    # 2. Renderização PDF
    # -----------------------------------------------------------
    def render_pdf(self, html_final: str, css_text: str, output_path: str) -> str:
        """
        Recebe:
            - html_final: HTML final produzido pelo ReportEngine
            - css_text : conteúdo CSS consolidado
            - output_path: onde salvar o PDF final

        Retorna:
            Caminho do arquivo PDF gerado
        """

        renderer = self._get_renderer()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        self.logger.log_start("html→pdf", self.renderer)
        self.resources.measure_start()

        renderer.render(html_final, css_text, Path(output_path))

        self.resources.measure_end()
        self.logger.log_end(output_path)

        return output_path
