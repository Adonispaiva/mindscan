# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\adapters\corporate_style_adapter.py
# Última atualização: 2025-12-11T09:59:21.120711

# -*- coding: utf-8 -*-
"""
corporate_style_adapter.py
--------------------------

Adaptador de estilos para padronizar HTML e CSS do MindScan Corporate
antes da renderização final.
"""

from typing import Dict


class CorporateStyleAdapter:

    @staticmethod
    def inject_branding(html: str, branding: Dict[str, str]) -> str:
        """
        Insere tokens de branding dinâmico no HTML final.
        """
        for key, value in branding.items():
            html = html.replace(f"{{{{brand:{key}}}}}", value)
        return html

    @staticmethod
    def adjust_for_pdf(html: str) -> str:
        """
        Ajusta detalhes do HTML para garantir compatibilidade total
        com o motor PDF (WeasyPrint).
        """
        html = html.replace("box-shadow:", "border:")
        html = html.replace("position: fixed;", "")
        return html

    @staticmethod
    def optimize_for_render(html: str) -> str:
        """
        Remove detalhes desnecessários e comprime espaçamentos.
        """
        while "  " in html:
            html = html.replace("  ", " ")
        return html.strip()
