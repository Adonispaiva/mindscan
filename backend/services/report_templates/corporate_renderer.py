# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report_templates\corporate_renderer.py
# Última atualização: 2025-12-11T09:59:21.292589

# -*- coding: utf-8 -*-
"""
MindScan — Corporate Renderer (Parte 1/2)
-----------------------------------------

Renderer oficial MindScan Corporate (HTML Premium + PDF via WeasyPrint).

Esta é a PARTE 1:
- Imports
- Classe
- Construtor
- CSS Premium
- HTML Builder completo
- Montagem das seções do Blueprint Corporate

Parte 2 entregará:
- PDF Builder (WeasyPrint)
- Finalização da classe
"""

import os
from typing import Any, Dict, List
from datetime import datetime

from services.helpers.report_utils import (
    clean_text,
    normalize_section,
    normalize_summary,
    prepare_payload_for_render,
)


class CorporateRenderer:
    """
    Renderer corporativo MindScan.
    Gera um HTML Premium estruturado segundo o blueprint oficial.
    PDF será gerado via WeasyPrint na Parte 2.
    """

    TEMPLATE_NAME = "corporate"

    def __init__(self, payload: Dict[str, Any], output_html: str, output_pdf: str):
        """
        payload: dict vindo de ReportPayload.to_render_dict()
        output_html: caminho onde o HTML será salvo
        output_pdf: caminho onde o PDF será gerado pela Parte 2
        """
        self.raw_payload = payload
        self.payload = prepare_payload_for_render(payload)
        self.output_html = output_html
        self.output_pdf = output_pdf

        # Extrair dados principais
        self.test_id = self.payload.get("test_id", "").upper()
        self.context = self.payload.get("context", {})
        self.sections = self.payload.get("sections", [])
        self.summary = self.payload.get("summary", {})

        self._html = ""

    # ----------------------------------------------------------------------
    # CSS Premium (corporativo, moderno, estilo SynMind Evolution)
    # ----------------------------------------------------------------------
    def _get_css(self) -> str:
        return """
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 40px;
                color: #222;
                line-height: 1.6;
            }
            h1, h2, h3 {
                color: #2B3A67;
                margin-bottom: 8px;
            }
            h1 {
                font-size: 32px;
                margin-top: 20px;
            }
            h2 {
                font-size: 24px;
                margin-top: 30px;
            }
            h3 {
                font-size: 20px;
                margin-top: 20px;
            }
            .section {
                margin-top: 35px;
                padding-bottom: 10px;
                border-bottom: 1px solid #ddd;
            }
            .label {
                font-weight: bold;
                color: #1A5276;
            }
            .key-point {
                margin: 6px 0;
                padding-left: 12px;
            }
            .risk {
                background: #fff4f4;
                border-left: 4px solid #d9534f;
                padding: 10px;
                margin: 8px 0;
            }
            .strength {
                background: #f4fff6;
                border-left: 4px solid #5cb85c;
                padding: 10px;
                margin: 8px 0;
            }
            .dev {
                background: #f7faff;
                border-left: 4px solid #0275d8;
                padding: 10px;
                margin: 8px 0;
            }
            .footer {
                margin-top: 60px;
                font-size: 12px;
                color: #777;
                text-align: center;
            }
        </style>
        """

    # ----------------------------------------------------------------------
    # Builder principal
    # ----------------------------------------------------------------------
    def build_html(self) -> str:
        """
        Gera o HTML final com todas as seções corporativas.
        (Parte 1/2 – PDF será feito na Parte 2)
        """

        html = "<html><head>"
        html += self._get_css()
        html += "</head><body>"

        html += self._render_cover()
        html += self._render_executive_summary()
        html += self._render_competencies()
        html += self._render_behavioral_patterns()
        html += self._render_risks()
        html += self._render_growth()
        html += self._render_culture()
        html += self._render_conclusion()

        html += "<div class='footer'>MindScan® Corporate — SynMind Technologies</div>"
        html += "</body></html>"

        self._html = html

        with open(self.output_html, "w", encoding="utf-8") as f:
            f.write(html)

        return html

    # ----------------------------------------------------------------------
    # CAPA
    # ----------------------------------------------------------------------
    def _render_cover(self) -> str:
        name = clean_text(self.context.get("name", ""))
        date = datetime.now().strftime("%d/%m/%Y")

        return f"""
        <div class='section'>
            <h1>MindScan Corporate Report</h1>
            <p><span class='label'>Avaliado:</span> {name}</p>
            <p><span class='label'>Data:</span> {date}</p>
            <p><span class='label'>ID da Avaliação:</span> {self.test_id}</p>
        </div>
        """

    # ----------------------------------------------------------------------
    # EXECUTIVE SUMMARY
    # ----------------------------------------------------------------------
    def _render_executive_summary(self) -> str:
        if not self.summary:
            return ""

        headline = clean_text(self.summary.get("headline", ""))
        overview = clean_text(self.summary.get("overview", ""))
        key_points = self.summary.get("key_points", [])

        html = "<div class='section'>"
        html += "<h2>Resumo Executivo</h2>"

        if headline:
            html += f"<p><strong>{headline}</strong></p>"

        if overview:
            html += f"<p>{overview}</p>"

        if key_points:
            html += "<h3>Pontos-Chave</h3>"
            for p in key_points:
                html += f"<p class='key-point'>• {clean_text(p)}</p>"

        html += "</div>"
        return html

    # ----------------------------------------------------------------------
    # COMPETÊNCIAS
    # ----------------------------------------------------------------------
    def _render_competencies(self) -> str:
        sec = self._get_section("competencias")
        if not sec:
            return ""

        html = "<div class='section'>"
        html += "<h2>Mapa de Competências</h2>"

        if sec.get("description"):
            html += f"<p>{sec['description']}</p>"

        for block in sec.get("blocks", []):
            title = clean_text(block.get("title", ""))
            content = clean_text(block.get("content", ""))

            html += f"<h3>{title}</h3>"
            if content:
                html += f"<p>{content}</p>"

        html += "</div>"
        return html

    # ----------------------------------------------------------------------
    # PADRÕES COMPORTAMENTAIS
    # ----------------------------------------------------------------------
    def _render_behavioral_patterns(self) -> str:
        sec = self._get_section("padroes_comportamentais")
        if not sec:
            return ""

        html = "<div class='section'>"
        html += "<h2>Padrões Comportamentais</h2>"

        if sec.get("description"):
            html += f"<p>{sec['description']}</p>"

        for block in sec.get("blocks", []):
            html += f"<h3>{clean_text(block.get('title',''))}</h3>"
            html += f"<p>{clean_text(block.get('content',''))}</p>"

        html += "</div>"
        return html

    # ----------------------------------------------------------------------
    # RISCOS
    # ----------------------------------------------------------------------
    def _render_risks(self) -> str:
        sec = self._get_section("riscos")
        if not sec:
            return ""

        html = "<div class='section'>"
        html += "<h2>Riscos e Blind Spots</h2>"

        for block in sec.get("blocks", []):
            html += "<div class='risk'>"
            html += f"<strong>{clean_text(block.get('title',''))}</strong><br>"
            html += f"{clean_text(block.get('content',''))}"
            html += "</div>"

        html += "</div>"
        return html

    # ----------------------------------------------------------------------
    # DESENVOLVIMENTO
    # ----------------------------------------------------------------------
    def _render_growth(self) -> str:
        sec = self._get_section("desenvolvimento")
        if not sec:
            return ""

        html = "<div class='section'>"
        html += "<h2>Potenciais de Desenvolvimento</h2>"

        for block in sec.get("blocks", []):
            html += "<div class='dev'>"
            html += f"<strong>{clean_text(block.get('title',''))}</strong><br>"
            html += f"{clean_text(block.get('content',''))}"
            html += "</div>"

        html += "</div>"
        return html

    # ----------------------------------------------------------------------
    # CULTURA
    # ----------------------------------------------------------------------
    def _render_culture(self) -> str:
        sec = self._get_section("cultura")
        if not sec:
            return ""

        html = "<div class='section'>"
        html += "<h2>Aderência Cultural</h2>"

        if sec.get("description"):
            html += f"<p>{sec['description']}</p>"

        for block in sec.get("blocks", []):
            html += f"<h3>{clean_text(block.get('title',''))}</h3>"
            html += f"<p>{clean_text(block.get('content',''))}</p>"

        html += "</div>"
        return html

    # ----------------------------------------------------------------------
    # CONCLUSÃO
    # ----------------------------------------------------------------------
    def _render_conclusion(self) -> str:
        sec = self._get_section("conclusao")
        if not sec:
            return ""

        html = "<div class='section'>"
        html += "<h2>Conclusão Executiva</h2>"

        for block in sec.get("blocks", []):
            html += f"<p>{clean_text(block.get('content',''))}</p>"

        html += "</div>"
        return html

    # ----------------------------------------------------------------------
    # Helper para buscar seção
    # ----------------------------------------------------------------------
    def _get_section(self, key: str) -> Dict[str, Any]:
        for sec in self.sections:
            if sec.get("id") == key:
                return sec
        return {}
# ----------------------------------------------------------------------
# PARTE 2 — PDF Builder (WeasyPrint) + Finalização da Classe
# ----------------------------------------------------------------------

from weasyprint import HTML, CSS

    # ----------------------------------------------------------------------
    # PDF BUILDER via WeasyPrint
    # ----------------------------------------------------------------------
    def build_pdf(self) -> str:
        """
        Converte o HTML premium em PDF corporativo.
        Necessita que self._html já esteja disponível (build_html).
        """

        if not self._html:
            # Se o HTML não foi gerado ainda, gera agora.
            self.build_html()

        try:
            HTML(string=self._html).write_pdf(self.output_pdf)
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar PDF com WeasyPrint: {e}")

        return self.output_pdf

    # ----------------------------------------------------------------------
    # EXPORTADOR COMPLETO (HTML + PDF)
    # ----------------------------------------------------------------------
    def export(self) -> Dict[str, str]:
        """
        Método unificado para uso pelo ReportService.
        Gera HTML + PDF e retorna os caminhos.
        """

        html_path = self.build_html()
        pdf_path = self.build_pdf()

        return {
            "html": self.output_html,
            "pdf": self.output_pdf
        }

    # ----------------------------------------------------------------------
    # Representação para debug
    # ----------------------------------------------------------------------
    def __repr__(self):
        return f"<CorporateRenderer test_id={self.test_id}>"


# ===========================
# FIM DA PARTE 2/2
# ===========================

