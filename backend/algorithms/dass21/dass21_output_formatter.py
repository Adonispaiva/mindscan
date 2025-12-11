# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\dass21\dass21_output_formatter.py
# Última atualização: 2025-12-11T09:59:20.667799

"""
DASS-21 Output Formatter
Formata os resultados do módulo DASS-21 para o padrão utilizado
pelo MindScanEngine, cruzamentos e relatórios.
"""

from typing import Dict, Any


class Dass21OutputFormatter:
    """
    Estrutura o payload final do DASS-21.
    """

    def __init__(self):
        self.version = "1.0"

    def format(
        self,
        normalized_scores: Dict[str, float],
        severity_levels: Dict[str, str],
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        normalized_scores:
            {"depressao": 0-100, "ansiedade": 0-100, "estresse": 0-100}

        severity_levels:
            {"depressao": "leve/moderado/..."}

        metadata:
            informações adicionais (raw_scores, validação, etc.)
        """
        return {
            "module": "DASS21",
            "version": self.version,
            "scores": normalized_scores,
            "severity": severity_levels,
            "metadata": metadata,
        }
