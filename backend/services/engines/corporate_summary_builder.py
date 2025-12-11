# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\engines\corporate_summary_builder.py
# Última atualização: 2025-12-11T09:59:21.151629

# -*- coding: utf-8 -*-
"""
corporate_summary_builder.py
----------------------------

Responsável por construir o Resumo Executivo do relatório Corporate.
Gera headline, overview e pontos-chave com base no payload.
"""

from typing import Dict, Any, List
from services.helpers.report_utils import clean_text


class CorporateSummaryBuilder:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload
        self.context = payload.get("context", {})

    def build_headline(self) -> str:
        name = clean_text(self.context.get("name", ""))
        return (
            f"{name} demonstra um perfil profissional consistente, "
            "com indicadores sólidos de desempenho, adaptabilidade e inteligência emocional."
        )

    def build_overview(self) -> str:
        return (
            "A análise integrada evidencia padrões comportamentais, competências centrais, "
            "potenciais de liderança, riscos e elementos de aderência à cultura organizacional."
        )

    def build_key_points(self) -> List[str]:
        return [
            "Demonstra estabilidade emocional e tomada de decisão racional.",
            "Mantém desempenho elevado em ambientes de pressão.",
            "Possui potencial para ampliar influência organizacional.",
        ]

    def build(self) -> Dict[str, Any]:
        return {
            "headline": self.build_headline(),
            "overview": self.build_overview(),
            "key_points": self.build_key_points(),
        }
