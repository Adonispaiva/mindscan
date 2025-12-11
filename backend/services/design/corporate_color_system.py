# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\design\corporate_color_system.py
# Última atualização: 2025-12-11T09:59:21.142708

# -*- coding: utf-8 -*-
"""
corporate_color_system.py
-------------------------

Sistema de cores corporativo do MindScan.
Fornece paletas, variações e tokens temáticos usados nos modelos HTML/PDF.
"""

from typing import Dict


class CorporateColorSystem:

    BASE_COLORS = {
        "primary": "#0066CC",
        "primary_dark": "#004C99",
        "primary_light": "#3385D6",

        "secondary": "#00A8A8",
        "secondary_dark": "#007F7F",
        "secondary_light": "#33C2C2",

        "neutral_100": "#FFFFFF",
        "neutral_200": "#F5F7FA",
        "neutral_300": "#E1E5EB",
        "neutral_400": "#C7CBD1",
        "neutral_700": "#4D4F52",
        "neutral_900": "#1C1D1F",
    }

    @classmethod
    def get(cls, key: str) -> str:
        return cls.BASE_COLORS.get(key, "#000000")

    @classmethod
    def palette(cls) -> Dict[str, str]:
        return cls.BASE_COLORS.copy()
