# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\design\corporate_layout_engine.py
# Última atualização: 2025-12-11T09:59:21.144688

# -*- coding: utf-8 -*-
"""
corporate_layout_engine.py
--------------------------

Engine de layout corporativo para relatórios HTML/PDF.
Responsável por:
- grid
- espaçamentos
- tipografia
- estilos visuais globais
"""

from typing import Dict, Any
from services.design.corporate_color_system import CorporateColorSystem


class CorporateLayoutEngine:

    @staticmethod
    def base_styles() -> Dict[str, Any]:
        """
        Retorna estilos fundamentais aplicados a todos os relatórios.
        """
        return {
            "font_family": "Inter, Arial, sans-serif",
            "heading_color": CorporateColorSystem.get("primary_dark"),
            "body_color": CorporateColorSystem.get("neutral_900"),
            "background_color": CorporateColorSystem.get("neutral_100"),

            "spacing_small": "8px",
            "spacing_medium": "16px",
            "spacing_large": "32px",

            "border_radius": "6px",
            "shadow_soft": "0 2px 6px rgba(0,0,0,0.08)",
        }

    @staticmethod
    def apply_to_context(context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insere estilos visuais dentro do contexto HTML.
        """
        context["styles"] = CorporateLayoutEngine.base_styles()
        return context
