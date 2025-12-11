# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\helpers\report_text_engine.py
# Última atualização: 2025-12-11T09:59:21.155629

# -*- coding: utf-8 -*-
"""
report_text_engine.py
---------------------

Engine oficial de textos MindScan Corporate.
Gera frases, insights e narrativa de alta qualidade.
"""

from typing import Dict, Any, List
from services.helpers.report_utils import clean_text


class ReportTextEngine:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload

    # --------------------------------------------------------------
    # Gera headline do resumo executivo
    # --------------------------------------------------------------
    def generate_headline(self) -> str:
        name = self.payload["context"].get("name", "")
        return f"{name} apresenta um perfil estratégico com pontos de força claros e áreas de desenvolvimento bem definidas."

    # --------------------------------------------------------------
    # Overview corporativo
    # --------------------------------------------------------------
    def generate_overview(self) -> str:
        return (
            "Este relatório oferece uma visão integrada do perfil comportamental, "
            "riscos organizacionais, potenciais de desenvolvimento e aderência cultural."
        )

    # --------------------------------------------------------------
    # Pontos-chave
    # --------------------------------------------------------------
    def generate_key_points(self) -> List[str]:
        return [
            "Demonstra capacidade consistente de adaptação em cenários complexos.",
            "Toma decisões com base em lógica e evidências, mantendo estabilidade emocional.",
            "Possui potencial para ampliar influência em ambientes de liderança.",
        ]

    # --------------------------------------------------------------
    # Riscos
    # --------------------------------------------------------------
    def generate_risk_block(self, title: str, content: str) -> Dict[str, str]:
        return {"title": clean_text(title), "content": clean_text(content)}

    # --------------------------------------------------------------
    # Crescimento
    # --------------------------------------------------------------
    def generate_growth_recommendation(self, title: str, content: str) -> Dict[str, str]:
        return {"title": clean_text(title), "content": clean_text(content)}

    # --------------------------------------------------------------
    # Cultura
    # --------------------------------------------------------------
    def generate_culture_fit(self, title: str, content: str) -> Dict[str, str]:
        return {"title": clean_text(title), "content": clean_text(content)}

