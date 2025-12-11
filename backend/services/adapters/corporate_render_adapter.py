# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\adapters\corporate_render_adapter.py
# Última atualização: 2025-12-11T09:59:21.120711

# -*- coding: utf-8 -*-
"""
corporate_render_adapter.py
---------------------------

Faz a ponte entre o Corporate Renderer e o motor de HTML/CSS.
Normaliza estrutura, aplica estilos, injeta branding,
e deixa o conteúdo pronto para renderização corporativa.
"""

from typing import Dict
from services.adapters.corporate_style_adapter import CorporateStyleAdapter
from services.report_branding import MindScanBranding


class CorporateRenderAdapter:

    @staticmethod
    def prepare_html(html: str) -> str:
        """
        Aplica:
        - branding
        - ajustes para PDF
        - otimizações finais
        """
        branding = {
            "product_name": MindScanBranding.get_token("product_name"),
            "footer": MindScanBranding.get_token("footer_text"),
            "primary_color": MindScanBranding.get_color("primary"),
        }

        html = CorporateStyleAdapter.inject_branding(html, branding)
        html = CorporateStyleAdapter.adjust_for_pdf(html)
        html = CorporateStyleAdapter.optimize_for_render(html)

        return html
