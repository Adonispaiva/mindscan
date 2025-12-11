# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\engines\corporate_competency_engine.py
# Última atualização: 2025-12-11T09:59:21.146688

# -*- coding: utf-8 -*-
"""
corporate_competency_engine.py
------------------------------

Engine especializado em construir o bloco "Competências" do relatório corporativo.
"""

from typing import Dict, Any, List
from services.helpers.report_utils import clean_text


class CorporateCompetencyEngine:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload

    def generate_block(self, title: str, content: str) -> Dict[str, str]:
        return {
            "title": clean_text(title),
            "content": clean_text(content)
        }

    def build(self) -> Dict[str, Any]:
        """
        Retorna estrutura final da seção de competências.
        """
        return {
            "id": "competencias",
            "title": "Mapa de Competências",
            "description": (
                "Esta seção descreve as competências que sustentam o desempenho "
                "profissional do avaliado, evidenciando pontos fortes e capacidades centrais."
            ),
            "blocks": [
                self.generate_block(
                    "Resolução de Problemas",
                    "Demonstra clareza lógica e eficiência na análise de problemas complexos."
                ),
                self.generate_block(
                    "Comunicação",
                    "Apresenta discurso claro, direto e adequado ao contexto organizacional."
                ),
                self.generate_block(
                    "Autogestão",
                    "Mantém organização, disciplina e estabilidade emocional, mesmo sob pressão."
                ),
            ]
        }
