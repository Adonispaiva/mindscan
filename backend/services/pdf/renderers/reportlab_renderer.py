#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reportlab_renderer.py — Renderer Fallback (ReportLab)
MindScan v2.0 — Leo Vinci (Inovexa)
----------------------------------------------------------------------
Função:
    - Atuar como fallback quando o WeasyRenderer não está disponível
    - Aceita HTML final (já montado pelo ReportEngine)
    - Gera PDF simples baseado em texto

Observação:
    - CSS é ignorado (ReportLab não interpreta), mas mantido na assinatura.
"""

from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import re


class ReportLabRenderer:
    """
    Renderer fallback oficial do MindScan.
    """

    def __init__(self, logger=None):
        self.logger = logger

        if self.logger:
            self.logger.warn("ATENÇÃO: Renderer ativo é ReportLab (fallback).")

    # ------------------------------------------------------------------
    # ASSINATURA PADRÃO (compatível com WeasyRenderer)
    # ------------------------------------------------------------------
    def render(self, html_final: str, css_text: str, output_path: Path):
        """
        Parâmetros:
            html_final: HTML completo do ReportEngine
            css_text: CSS carregado (ignorado)
            output_path: destino do PDF

        Retorno:
            Caminho final do PDF
        """

        if self.logger:
            self.logger.info("Renderizando PDF via ReportLab (fallback).")
            self.logger.info(f"Arquivo de saída: {output_path}")

        try:
            texto = self._sanitize_html(html_final)
            self._generate_pdf(texto, output_path)

            if self.logger:
                self.logger.info("Renderização concluída (ReportLab fallback).")

            return output_path

        except Exception as e:
            if self.logger:
                self.logger.evento_erro("ReportLabRenderer.render", e)
            raise e

    # ------------------------------------------------------------------
    # Sanitização avançada de HTML
    # ------------------------------------------------------------------
    def _sanitize_html(self, html: str) -> str:
        """
        Remove tags HTML mantendo espaçamento mínimo.
        """
        texto = html

        # Remover scripts e estilos
        texto = re.sub(r"<(script|style).*?>.*?</\\1>", "", texto, flags=re.DOTALL)

        # Quebras estratégicas
        texto = texto.replace("<p", "\n<p")
        texto = texto.replace("<tr", "\n<tr")
        texto = texto.replace("<li", "\n• ")

        # Remover tags
        texto = re.sub(r"<[^>]+>", "", texto)

        # Normalizar múltiplas quebras
        texto = re.sub(r"\n\s*\n", "\n", texto)

        return texto.strip()

    # ------------------------------------------------------------------
    # Geração do PDF (texto puro)
    # ------------------------------------------------------------------
    def _generate_pdf(self, text: str, output_path: Path):
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

            c.drawString(x, y, linha[:120])
            y -= 6 * mm

        c.save()
