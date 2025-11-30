#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reportlab_renderer.py — Renderer Fallback usando ReportLab
-----------------------------------------------------------

Versão integrada ao Logger:
- Registra fallback em uso
- Registra caminhos
- Registra erros
"""

from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import re


class ReportLabRenderer:
    def __init__(self, templates_dir: Path, logger=None):
        """
        Mantém compatibilidade com a assinatura do WeasyRenderer.
        """
        self.templates_dir = Path(templates_dir)
        self.logger = logger

        if self.logger:
            self.logger.warn("ATENÇÃO: Utilizando renderer fallback (ReportLab).")

    # --------------------------------------------------------------
    # Renderização fallback simples
    # --------------------------------------------------------------
    def render_html_to_pdf(self, conteudo_html: str, output_path: Path):
        """
        Converte HTML final em PDF simples (texto puro).
        """

        if self.logger:
            self.logger.info("Renderizando PDF via ReportLab (fallback).")
            self.logger.info(f"Arquivo de saída: {output_path}")

        try:
            text = self._sanitize_html(conteudo_html)

            c = canvas.Canvas(str(output_path), pagesize=A4)
            width, height = A4

            x = 20 * mm
            y = height - 25 * mm

            c.setFont("Helvetica", 11)

            for linha in text.split("\n"):
                if y < 20 * mm:
                    c.showPage()
                    c.setFont("Helvetica", 11)
                    y = height - 20 * mm

                c.drawString(x, y, linha[:110])
                y -= 6 * mm

            c.save()

            if self.logger:
                self.logger.info("Renderização concluída (ReportLab).")

            return output_path

        except Exception as e:
            if self.logger:
                self.logger.evento_erro("ReportLabRenderer.render_html_to_pdf", e)
            raise e

    # --------------------------------------------------------------
    # Sanitização de HTML para texto simples
    # --------------------------------------------------------------
    def _sanitize_html(self, html: str) -> str:
        """
        Remove tags HTML.
        """
        texto = html
        texto = re.sub(r"<(script|style).*?>.*?</\\1>", "", texto, flags=re.DOTALL)
        texto = texto.replace("<p", "\n<p")
        texto = texto.replace("<tr", "\n<tr")
        texto = re.sub(r"<[^>]+>", "", texto)
        texto = re.sub(r"\n\s*\n", "\n", texto)
        return texto.strip()
