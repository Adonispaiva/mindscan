#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
weasy_renderer.py — Renderer WeasyPrint (MindScan v2.0)
Autor: Leo Vinci (Inovexa)
----------------------------------------------------------------------
Função:
    - Recebe o HTML FINAL do ReportEngine
    - Aplica o CSS consolidado
    - Gera o PDF usando WeasyPrint

Observação:
    — NÃO carrega mais base.html
    — NÃO substitui placeholders
    — Tudo já chega pronto do ReportEngine
"""

from pathlib import Path
from weasyprint import HTML, CSS


class WeasyRenderer:
    """
    Renderer oficial do MindScan usando WeasyPrint.
    HTML final é recebido já estruturado pelo ReportEngine.
    """

    def __init__(self, logger=None):
        self.logger = logger

        if self.logger:
            self.logger.info("WeasyRenderer v2.0 inicializado.")

    # ------------------------------------------------------------------
    # Renderização final para PDF
    # ------------------------------------------------------------------
    def render(self, html_final: str, css_text: str, output_path: Path):
        """
        html_final: HTML completo gerado pelo ReportEngine
        css_text: conteúdo do estilo retornado por CSS_STYLE_LOADER()
        output_path: onde salvar o PDF gerado
        """

        if self.logger:
            self.logger.info("Iniciando renderização PDF (WeasyPrint v2.0)...")
            self.logger.info(f"Arquivo de saída: {output_path}")

        try:
            # CSS como stylesheet temporário
            css_obj = CSS(string=css_text)

            # Gerar PDF
            HTML(string=html_final).write_pdf(
                str(output_path),
                stylesheets=[css_obj]
            )

            if self.logger:
                self.logger.info("Renderização concluída com sucesso (WeasyPrint v2.0).")

            return output_path

        except Exception as e:
            if self.logger:
                self.logger.evento_erro("WeasyRenderer.render", e)
            raise e
