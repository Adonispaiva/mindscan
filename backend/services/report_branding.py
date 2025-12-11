# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report_branding.py
# Última atualização: 2025-12-11T09:59:21.105108

# -*- coding: utf-8 -*-
"""
report_branding.py
------------------

Define tokens visuais, cores, logos e identidade oficial do MindScan Corporate.
"""

class MindScanBranding:

    COLORS = {
        "primary": "#2B3A67",
        "secondary": "#1A4C85",
        "accent": "#0275d8",
        "risk": "#d9534f",
        "growth": "#5cb85c",
        "neutral": "#8992A3",
    }

    LOGOS = {
        "synmind": "assets/report/synmind_logo.png",
        "mindscan": "assets/report/mindscan_logo.png"
    }

    TOKENS = {
        "product_name": "MindScan Corporate",
        "company": "SynMind Technologies",
        "footer_text": "MindScan® Corporate — SynMind Technologies"
    }

    @staticmethod
    def get_color(name: str) -> str:
        return MindScanBranding.COLORS.get(name, "#000000")

    @staticmethod
    def get_logo(name: str) -> str:
        return MindScanBranding.LOGOS.get(name, "")

    @staticmethod
    def get_token(name: str) -> str:
        return MindScanBranding.TOKENS.get(name, "")
